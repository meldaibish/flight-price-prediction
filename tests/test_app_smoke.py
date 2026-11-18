"""Run the UI path with a small Streamlit shim when Streamlit is unavailable.

This checks the model/loading/input/prediction integration, not web-browser rendering.
"""
from contextlib import nullcontext
from datetime import date, time
from pathlib import Path
import runpy
import sys
from types import SimpleNamespace


def test_streamlit_prediction_flow(monkeypatch):
    events = []

    class FakeStreamlit:
        cache_resource = staticmethod(lambda fn: fn)
        cache_data = staticmethod(lambda fn: fn)
        def set_page_config(self, **kwargs): pass
        def title(self, *args, **kwargs): pass
        def write(self, *args, **kwargs): pass
        def warning(self, *args, **kwargs): pass
        def caption(self, *args, **kwargs): pass
        def divider(self, *args, **kwargs): pass
        def form(self, *args, **kwargs): return nullcontext()
        def columns(self, n): return tuple(nullcontext() for _ in range(n))
        def expander(self, *args, **kwargs): return nullcontext()
        def dataframe(self, *args, **kwargs): pass
        def selectbox(self, text, options, **kwargs): return list(options)[0]
        def date_input(self, text, value, **kwargs): return value
        def time_input(self, text, value, **kwargs): return value
        def form_submit_button(self, *args, **kwargs): return True
        def metric(self, title, value, **kwargs): events.append((title, value))
        def error(self, value): raise AssertionError(value)
        def stop(self): raise AssertionError("Missing model or metadata")

    monkeypatch.setitem(sys.modules, "streamlit", FakeStreamlit())
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "flight_app.py"), run_name="__main__")
    assert len(events) == 1
    assert events[0][0] == "Estimated fare"
    assert "₹" in events[0][1]
