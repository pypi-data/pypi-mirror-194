###############################################################################
# Imports
###############################################################################
import gc
import textwrap

import matplotlib.pyplot as plt     # type: ignore
import matplotlib.ticker as ticker  # type: ignore
import multiprocessing as mp

from os import cpu_count
from time import perf_counter_ns
from typing import Any, Callable, Iterable, Sequence

from pybenchmarker._progress import progress


###############################################################################
# BenchmarkN Class
###############################################################################
class BenchmarkN:
    """
    Benchmark a sequence of functions over increasing input sizes.

    kwargs:
        functions:
            A nonempty sequence of one-argument functions to benchmark.
        argfunc:
            A one-argument function mapping a given input size to an input that
            will be passed to the functions to benchmark. For a given input
            size, `argfunc` is called only once to retrieve the input, which is
            subsequently reused for each function. This can cause problems if
            one wants to use an iterator as an input (or recursively).
        sizes:
            A (strictly increasing) nonempty sequence of input sizes to
            supply to `argfunc`. This MUST be supplied either through
            decorating `argfunc` with `@sizes(sequence)`, or through this
            argument.
        parallel:
            If `True`, parallelize the benchmarks using `processes` processes.
            Default is `False`.
        processes:
            If `parallel` is `True`, the number of processes to use for the
            benchmarks. Must satisfy `1 < processes <= os.cpu_count()`.
        threshold:
            The approximate number of nanoseconds (1s == 1E+9ns) to spend
            benchmarking a function (for a given input). Default is
            400_000_000ns or 0.4s.
        min_runs:
            Minimum number of runs per function per input. Default is `None`.
        key:
            For each input size, each function may be timed a number of times.
            The key function accepts an iterable of timings and outputs a
            single representative time to use for reporting. Defaults to the
            `min` built-in function. Example: `key=statistics.mean(x)`. This
            is only called if the calibrated number of runs for the function
            exceeds one; otherwise, key is treated as the identity function.
    """
    # Cycle through these colors for the lines
    COLORS: Sequence[str] = ['#79c0ff',
                             '#8957e5',  # d2a8ff
                             '#f0883e',  # ffa657
                             '#da3633',
                             '#8b949e',
                             '#3fb950',
                             '#FFD700',
                             '#00FF00',
                             '#FF1493',
                             '#8A2BE2',
                             '#7FFFD4']
    BCOLOR: str = "#0d1117"  # Background Color
    COLOR: str = "#8b949e"   # Text, Ticks, Etc.
    # Convert nanoseconds (ns) to ns, us, ms, or s
    SCALE_FACTORS: dict[str, int | float] = {"ns": 1, "us": 1e3, "ms": 1e6,
                                             "s": 1e9}

    timer: Callable[[], int] = perf_counter_ns

    def __init__(self, *,
                 functions: Sequence[Callable[[Any], Any]],
                 argfunc: Callable[[int], Any],
                 sizes: Sequence[int] | None = None,
                 threshold: int = 400_000_000,
                 min_runs: int | None = None,
                 parallel: bool = False,
                 processes: int | None = None,
                 key: Callable[[Iterable[int]], int | float] = min,
                 assert_equal: bool = False):
        self.functions = functions
        self.argfunc = argfunc

        # @sizes(x) decorator used?
        if hasattr(self.argfunc, "_sizes"):
            self._sizes = self.argfunc._sizes
        else:
            if sizes is None:
                raise ValueError("`sizes` must be a nonempty sequence of ints")
            self._sizes = sizes

        self.threshold = threshold
        self.min_runs = min_runs or 1

        # Parallelization enabled?
        if parallel:
            if not (count := cpu_count()):
                # CPU count undetermined
                self.parallel = False
            elif isinstance(processes, int) and 1 < processes <= count:
                self.parallel = True
                self.processes = processes
            else:
                raise ValueError("1 < processes <= os.cpu_count() required")
        else:
            self.parallel = False

        self.key = key
        self.assert_equal = assert_equal

        # key -> size, value -> sequence of timings corresp. 1-1 w/ `functions`
        self.results:  dict[int, Sequence[int | float]] = {}

    def _measure_timings(self, func: Callable[[Any], Any], arg: Any,
                         n_runs: int) -> list[int]:
        timings = []
        for i in range(n_runs):
            # No performance difference if gc calls wrap the loop instead
            gc.disable()
            try:
                start_time = self.timer()
                func(arg)
                end_time = self.timer()
            finally:
                gc.enable()

            timings.append(end_time - start_time)

        return timings

    def _time_func(self, func: Callable[[Any], Any],
                   arg: Any) -> tuple[int | float, Any]:
        gc.disable()
        try:
            start_time = self.timer()
            ret = func(arg)
            end_time = self.timer()
        finally:
            gc.enable()

        result = end_time - start_time

        n_runs = max((self.threshold - result) // result, self.min_runs - 1)

        if n_runs <= 0:
            return result, ret
        else:
            timings = self._measure_timings(func, arg, n_runs)
            timings.append(result)
            return self.key(timings), ret

    def _run_size(self, size: int) -> tuple[int, Sequence[int | float]]:
        # TODO: what if `arg` an iterator? And recursively.
        arg = self.argfunc(size)

        timings = []
        rets = []
        for func in self.functions:
            timing, ret = self._time_func(func, arg)
            timings.append(timing)
            rets.append(ret)

        if self.assert_equal and rets.count(rets[0]) != len(rets):
            raise AssertionError(f"Functions do not return the same value with"
                                 f" input size {size}")

        return size, timings

    def run(self) -> dict[int, Sequence[int | float]]:
        """
        Return a `dict` mapping input sizes to a sequence of timings
        corresponding to the functions supplied through the `functions`
        argument of the `__init__()` method.
        """
        if self.parallel:
            with mp.Pool(self.processes) as pool:
                results_iter = progress(pool.imap_unordered(self._run_size,
                                                            self._sizes),
                                        iterations=len(self._sizes))
                self.results = dict(results_iter)
        else:
            self.results = dict(progress(map(self._run_size, self._sizes),
                                         iterations=len(self._sizes)))

        return self.results

    def plot(self, *,
             xlabel: str = "size",
             title: str = "",
             unit_y: str = "ns",
             base_x: int = 10,
             base_y: int = 10,
             # matplotlib's savefig(fname, **kwargs)
             fname: str | None = None,
             **kwargs: Any
             ) -> None:
        if not self.results:
            self.run()

        try:
            yscale_factor = self.SCALE_FACTORS[unit_y]
        except KeyError:
            raise ValueError(f"Unsupported unit '{unit_y}'")

        fig, ax = plt.subplots()

        ax.set_prop_cycle(color=self.COLORS)

        # Make legend show function names by slowest to fastest (topdown)
        scaled_data = {}
        last_data = {}
        for idx, func in enumerate(self.functions):
            scaled_data[func] = [self.results[n][idx] / yscale_factor
                                 for n in self._sizes]
            last_data[func] = scaled_data[func][-1]
        slast_data = {k: v for k, v in sorted(last_data.items(),
                                              key=lambda item: -item[1])}

        # Plot data
        for func in slast_data:
            ax.plot(self._sizes, scaled_data[func], label=func.__name__)

        ax.set_xscale("log", base=base_x)
        ax.set_yscale("log", base=base_y)

        ax.xaxis.set_minor_locator(ticker.NullLocator())
        ax.yaxis.set_minor_locator(ticker.NullLocator())

        legend = ax.legend()
        legend.get_frame().set_alpha(0)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_xlabel(xlabel, color=self.COLOR)
        ax.set_ylabel(f"Time ({unit_y})", color=self.COLOR, rotation=0,
                      labelpad=0, y=1)

        ax.set_title(textwrap.fill(title, width=50), color=self.COLOR)

        ax.tick_params(axis="x", colors=self.COLOR)
        ax.tick_params(axis="y", colors=self.COLOR)

        for text in legend.get_texts():
            text.set_color(self.COLOR)

        fig.set_facecolor(self.BCOLOR)  # Outer
        ax.set_facecolor(self.BCOLOR)   # Inner

        if fname:
            fig.savefig(fname, **kwargs)

        plt.show()

    @staticmethod
    def sizes(x: Sequence[int]) -> Callable[[Callable[..., Any]],
                                            Callable[..., Any]]:
        """
        @sizes(x) sets the decorated function's _sizes attribute to x.

        @sizes(x)
        def arg(n):  <==>  def arg(n):
            pass               pass
                           arg = sizes(x)(arg)
        """
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            setattr(func, '_sizes', x)
            return func
        return decorator
