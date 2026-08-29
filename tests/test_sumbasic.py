from pathlib import Path;
from sumbasic import BasicInterpreter, BasicProgram;


def runner(source):
    output = [];
    def emit(text, end="\n"):
        output.append(str(text) + end);
    basic = BasicInterpreter(input_func=lambda prompt="": "Test", output_func=emit);
    basic.program.load_text(source);
    basic.run();
    return basic, "".join(output);


def test_numbered_program_and_for_next():
    basic, out = runner('10 A%=1\n20 FOR I%=1 TO 3\n30 PRINT I%;\n40 NEXT I%\n50 END\n');
    assert out == '123';


def test_string_suffix_and_functions():
    basic, out = runner('A$="hello"\nPRINT UCASE$(A$)\n');
    assert out == 'HELLO\n';


def test_if_block():
    basic, out = runner('A=2\nIF A > 1 THEN\nPRINT "yes"\nELSE\nPRINT "no"\nEND IF\n');
    assert out == 'yes\n';


def test_gosub_return():
    basic, out = runner('10 GOSUB 100\n20 PRINT "done"\n30 END\n100 PRINT "sub"\n110 RETURN\n');
    assert out == 'sub\ndone\n';


def test_data_read():
    basic, out = runner('10 DATA "Ada", 5\n20 READ N$, X%\n30 PRINT N$; X%\n');
    assert out == 'Ada5\n';


def test_renum_rewrites_goto():
    p = BasicProgram(); p.load_text('10 GOTO 30\n30 END\n'); p.renumber(100, 100);
    assert p.source_text() == '100 GOTO 200\n200 END\n';


def test_immediate_numbered_lines():
    b = BasicInterpreter(output_func=lambda *a, **k: None); b.execute_immediate('10 PRINT "A"'); b.execute_immediate('20 END');
    assert '10 PRINT "A"' in b.program.source_text();


def test_strings_are_not_rewritten_as_operators():
    basic, out = runner('PRINT "A=B and name$ stays literal"\n');
    assert out == 'A=B and name$ stays literal\n';


def test_while_loop():
    basic, out = runner('A%=1\nWHILE A% <= 3\nPRINT A%;\nA%=A%+1\nWEND\n');
    assert out == '123';
