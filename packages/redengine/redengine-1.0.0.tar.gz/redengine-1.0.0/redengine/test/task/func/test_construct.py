
from pathlib import Path
import types

import pytest

from redengine.tasks import FuncTask
from redengine.conditions import AlwaysFalse, AlwaysTrue, DependSuccess

def myfunc(): ...

@pytest.mark.parametrize("execution", ["main", "thread", "process"])
def test_construct(tmpdir, session, execution):

    # Going to tempdir to dump the log files there
    with tmpdir.as_cwd() as old_dir:
        if execution == "process":
            with pytest.raises(AttributeError):
                # Unpicklable function (cannot use process)
                task = FuncTask(lambda : None, execution=execution)
        else:
            task = FuncTask(lambda : None, execution=execution)
            
        # This should always be picklable
        task = FuncTask(myfunc, execution=execution)
        assert not task.is_delayed()
        assert task.status is None

@pytest.mark.parametrize("execution", ["main", "thread", "process"])
def test_construct_delayed(tmpdir, session, execution):

    # Going to tempdir to dump the log files there
    with tmpdir.as_cwd() as old_dir:
        task = FuncTask("myfunc", path="myfile.py", execution=execution)
        assert task.status is None
        assert task.is_delayed()
        assert task.func_name == "myfunc"
        assert task.path == Path("myfile.py")
        assert task._func is None

def test_construct_decorate(tmpdir, session):
    # Going to tempdir to dump the log files there
    with tmpdir.as_cwd() as old_dir:


        @FuncTask(start_cond=AlwaysTrue(), name="mytask", execution="main")
        def do_stuff():
            pass
        
        assert isinstance(do_stuff, types.FunctionType)

        do_stuff_task = session.tasks["mytask"]
        assert isinstance(do_stuff_task, FuncTask)
        assert do_stuff_task.status is None
        assert do_stuff_task.start_cond == AlwaysTrue()
        assert do_stuff_task.name == "mytask"

        assert {"mytask": do_stuff_task} == session.tasks 

def test_construct_decorate_minimal(tmpdir, session):
    """This is an exception when FuncTask returns itself 
    (__init__ cannot return anything else)"""
    # Going to tempdir to dump the log files there
    orig_default_exec = FuncTask.default_execution
    FuncTask.default_execution = "main"
    try:
        with tmpdir.as_cwd() as old_dir:

            @FuncTask
            def do_stuff():
                pass

            assert isinstance(do_stuff, FuncTask)
            assert do_stuff.status is None
            assert do_stuff.start_cond == AlwaysFalse()
            assert do_stuff.name.endswith(":do_stuff")

            assert [do_stuff] == list(session.tasks.values())
    finally:
        FuncTask.default_execution = orig_default_exec

def test_construct_decorate_default_name(tmpdir, session):
    # Going to tempdir to dump the log files there
    with tmpdir.as_cwd() as old_dir:


        @FuncTask(start_cond=AlwaysTrue(), execution="main")
        def do_stuff():
            pass
        
        assert isinstance(do_stuff, types.FunctionType)
        do_stuff_task = list(session.tasks.values())[-1]
        assert isinstance(do_stuff_task, FuncTask)
        assert do_stuff_task.status is None
        assert do_stuff_task.start_cond == AlwaysTrue()
        assert do_stuff_task.name.endswith(":do_stuff")

        assert [do_stuff_task] == list(session.tasks.values())

@pytest.mark.parametrize(
    "start_cond,depend,expected",
    [
        pytest.param(
            AlwaysTrue(),
            None,
            AlwaysTrue(),
            id="AlwaysTrue"),
        pytest.param(
            AlwaysTrue(),
            ["another task"],
            AlwaysTrue() & DependSuccess(task="task", depend_task="another task"),
            id="AlwaysTrue with dependent"),
    ],
)
def test_set_start_condition(tmpdir, start_cond, depend, expected, session):

    # Going to tempdir to dump the log files there
    with tmpdir.as_cwd() as old_dir:

        task = FuncTask(
            lambda : None, 
            name="task",
            start_cond=start_cond,
            dependent=depend,
            execution="main",
        )
        assert expected == task.start_cond


@pytest.mark.parametrize(
    "start_cond_str,start_cond",
    [
        pytest.param("true", lambda: AlwaysTrue(), id="true"),
        pytest.param("always true & always true", lambda: AlwaysTrue() & AlwaysTrue(), id="always true & always true"),
    ],
)
def test_set_start_condition_str(tmpdir, start_cond_str, start_cond, session):

    # Going to tempdir to dump the log files there
    with tmpdir.as_cwd() as old_dir:

        task = FuncTask(
            lambda : None, 
            name="task",
            start_cond=start_cond_str,
            execution="main",
        )
        assert start_cond() == task.start_cond

        assert str(task.start_cond) == start_cond_str