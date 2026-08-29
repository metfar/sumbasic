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


def test_power_operator_immediate():
    output = [];
    b = BasicInterpreter(output_func=lambda text, end="\n": output.append(str(text) + end));
    b.execute_immediate('? 5^3');
    assert ''.join(output) == '125\n';


def test_sequential_file_io(tmp_path):
    path = tmp_path / 'seq.txt';
    source = 'OPEN "{}" FOR OUTPUT AS #1\nWRITE #1, "Ada", 42\nCLOSE #1\nOPEN "{}" FOR INPUT AS #A\nINPUT #A, N$, X%\nCLOSE #A\nPRINT N$; X%\n'.format(path, path);
    basic, out = runner(source);
    assert out == 'Ada42\n';
    assert path.read_text() == 'Ada,42\n';


def test_line_input_and_fopen_style_mode(tmp_path):
    path = tmp_path / 'lines.txt'; path.write_text('hello world\n');
    basic, out = runner('OPEN "{}" MODE "r" AS #1\nLINE INPUT #1, A$\nCLOSE #1\nPRINT A$\n'.format(path));
    assert out == 'hello world\n';


def test_random_file_fields(tmp_path):
    path = tmp_path / 'records.dat';
    source = '''OPEN "{}" FOR RANDOM AS #1 LEN=12
FIELD #1, 8 AS NAME$, 4 AS CODE$
NAME$="ADA": CODE$="42"
PUT #1, 1
NAME$="": CODE$=""
GET #1, 1
CLOSE #1
PRINT NAME$; ":"; CODE$
'''.format(path);
    basic, out = runner(source);
    assert out == 'ADA:42\n';
    assert path.read_bytes() == b'ADA     42  ';


def test_freefile_eof_lof_loc(tmp_path):
    path = tmp_path / 'data.txt'; path.write_text('x\n');
    basic, out = runner('OPEN "{}" FOR INPUT AS #1\nPRINT FREEFILE()\nPRINT LOF(1)\nLINE INPUT #1, A$\nPRINT EOF(1)\nCLOSE #1\n'.format(path));
    lines = out.splitlines();
    assert lines[0] == '2';
    assert lines[1] == '2';
    assert lines[2] == 'True';


def test_named_standard_stream_channels():
    import io;
    from sumbasic.channels import ChannelManager;
    output = io.StringIO();
    b = BasicInterpreter(output_func=lambda *args, **kwargs: None);
    b.channels = ChannelManager(stdin=io.StringIO('Ada\n'), stdout=output, stderr=io.StringIO());
    b.execute_immediate('OPEN STDIN FOR INPUT AS #1');
    b.execute_immediate('LINE INPUT #1, NAME$');
    b.execute_immediate('OPEN STDOUT FOR OUTPUT AS #2');
    b.execute_immediate('PRINT #2, NAME$');
    assert output.getvalue() == 'Ada\n';


def test_channel_letters_are_select_style_aliases():
    from sumbasic.channels import channel_number;
    assert channel_number('A') == 1;
    assert channel_number('J') == 10;
    assert channel_number('#3') == 3;


def test_db_bridge_object_available():
    b = BasicInterpreter(output_func=lambda *args, **kwargs: None);
    db = b._db();
    assert db.select('A') == 1;
    assert db.area == 1;
    db.close();


def test_sumtui_console_statusbar_api_regression():
    from sumbasic.console import SumBasicConsoleApp;
    output = [];
    b = BasicInterpreter(output_func=lambda text, end="\n": output.append(str(text) + end));
    app = SumBasicConsoleApp(interpreter=b);
    app._submit('? 5^3', app.command);
    assert app.status.text.startswith('Ready.');
    assert ''.join(output) == '125\n';


def test_input_pipeline_channel():
    output = [];
    b = BasicInterpreter(output_func=lambda text, end="\n": output.append(str(text) + end));
    b.program.load_text('OPEN "| printf \'Ada\\n\'" FOR INPUT AS #1\nLINE INPUT #1, N$\nCLOSE #1\nPRINT N$\n');
    b.run();
    assert ''.join(output) == 'Ada\n';
