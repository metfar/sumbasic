from pathlib import Path;
from sumbasic import BasicError, BasicInterpreter, BasicProgram;


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


def test_pi_is_spectrum_constant_and_immutable():
    from sumbasic.expressions import BasicExpressionError;
    basic, out = runner('PRINT PI\n');
    assert out == '3.1415927\n';
    try:
        basic.execute_immediate('PI = 3');
        assert False, 'PI assignment should fail';
    except BasicExpressionError:
        pass;


def test_hash_apostrophe_and_rem_comments():
    basic, out = runner('A!=2 # modern comment\nPRINT A! \' classic comment\nREM old comment\nPRINT "# stays in strings"\n');
    assert out == '2\n# stays in strings\n';


def test_modern_suffix_mapping_integer_and_double():
    basic, out = runner('A!=3.9\nB%=3\nPRINT A!; ","; B% / 2\n');
    assert basic.variables['a!'] == 3;
    assert isinstance(basic.variables['a!'], int);
    assert isinstance(basic.variables['b%'], float);
    assert out == '3,1.5\n';


def test_data_is_literal_and_restore_to_line():
    source = '''10 A!=99
20 DATA A!, "first", 10
30 DATA "second", 20
40 READ X$, Y$, N!
50 RESTORE 30
60 READ Z$, M!
70 PRINT X$; ":"; Y$; ":"; N!; ":"; Z$; ":"; M!
''';
    basic, out = runner(source);
    assert out == 'A!:first:10:second:20\n';


def test_multidimensional_classic_array_and_bounds():
    source = '''DIM A$(5, 7, 3, 8)
A$(2, 4, 1, 6) = "X"
PRINT A$(2, 4, 1, 6)
PRINT LBOUND(A$, 1); ":"; UBOUND(A$, 1); ":"; UBOUND(A$, 4)
''';
    basic, out = runner(source);
    assert out == 'X\n0:5:8\n';
    assert basic.arrays['a$'].dimensions == 4;


def test_explicit_bounds_and_option_base():
    source = '''OPTION BASE 1
DIM A!(5, 2 TO 4)
A!(1, 2)=7
PRINT LBOUND(A!,1); ":"; UBOUND(A!,1); ":"; LBOUND(A!,2); ":"; UBOUND(A!,2); ":"; A!(1,2)
''';
    basic, out = runner(source);
    assert out == '1:5:2:4:7\n';


def test_dim_shared_and_modern_collections():
    source = '''DIM SHARED Font AS DICT
DIM Rows AS LIST
Rows = [4, 10, 17]
Font["A"] = Rows
PRINT LEN(Font["A"])
FOR EACH N! IN Font["A"]
PRINT N!;
NEXT N!
''';
    basic, out = runner(source);
    assert out == '3\n41017';
    assert 'font' in basic.shared_variables;
    assert basic.variables['font']['A'] == [4, 10, 17];


def test_collection_methods():
    basic, out = runner('DIM Names AS LIST\nNames.APPEND("Ada")\nNames.APPEND("Linus")\nPRINT Names[1]\n');
    assert out == 'Linus\n';


def test_graphics_are_reserved_stubs():
    basic, out = runner('SCREEN 1\nCIRCLE 100, 100, 20\nRECTANGLE 1, 1, 10, 10\n');
    assert out == 'SCREEN: NOT IMPLEMENTED YET\nCIRCLE: NOT IMPLEMENTED YET\nRECTANGLE: NOT IMPLEMENTED YET\n';


def test_bare_inkey_function():
    output = [];
    basic = BasicInterpreter(output_func=lambda text, end="\n": output.append(str(text) + end), inkey_func=lambda: "K");
    basic.program.load_text('PRINT INKEY$\n');
    basic.run();
    assert ''.join(output) == 'K\n';


def test_complete_arithmetic_operator_family():
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    assert expr.eval('2 + 3 * 4') == 14;
    assert expr.eval('(2 + 3) * 4') == 20;
    assert expr.eval('7 / 2') == 3.5;
    assert expr.eval(r'7\2') == 3;
    assert expr.eval('7 DIV 2') == 3;
    assert expr.eval('7 MOD 3') == 1;
    assert expr.eval('2^8') == 256;
    assert expr.eval('1 << 5') == 32;
    assert expr.eval('32 >> 3') == 4;
    assert expr.eval('5 XOR 3') == 6;
    assert expr.eval('&B1010 + &H10 + &O10') == 34;


def test_relational_and_logical_operators():
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    assert expr.eval('2 = 2') is True;
    assert expr.eval('2 <> 3') is True;
    assert expr.eval('2 < 3') is True;
    assert expr.eval('2 <= 2') is True;
    assert expr.eval('3 >= 2') is True;
    assert expr.eval('3 > 2') is True;
    assert expr.eval('NOT FALSE') is True;
    assert expr.eval('TRUE AND FALSE') is False;
    assert expr.eval('TRUE OR FALSE') is True;
    assert expr.eval('TRUE XOR FALSE') is True;


def test_spectrum_and_extended_transcendental_math():
    import math;
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    assert math.isclose(expr.eval('SIN(PI/2)'), 1.0, rel_tol=0.0, abs_tol=1e-6);
    assert math.isclose(expr.eval('COS(0)'), 1.0);
    assert math.isclose(expr.eval('TAN(0)'), 0.0);
    assert math.isclose(expr.eval('ASN(1)'), math.pi / 2);
    assert math.isclose(expr.eval('ACS(1)'), 0.0);
    assert math.isclose(expr.eval('ATN(1)'), math.pi / 4);
    assert math.isclose(expr.eval('ATN2(1,1)'), math.pi / 4);
    assert math.isclose(expr.eval('LN(EXP(1))'), 1.0);
    assert math.isclose(expr.eval('LOG10(1000)'), 3.0);
    assert math.isclose(expr.eval('LOG2(8)'), 3.0);
    assert math.isclose(expr.eval('LOG(1000)'), 3.0);
    assert math.isclose(expr.eval('LOGB(81,3)'), 4.0);
    assert math.isclose(expr.eval('SINH(0)'), 0.0);
    assert math.isclose(expr.eval('COSH(0)'), 1.0);
    assert math.isclose(expr.eval('TANH(0)'), 0.0);


def test_roots_rounding_and_range_math():
    import math;
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    assert expr.eval('SQR(81)') == 9.0;
    assert math.isclose(expr.eval('CBRT(-8)'), -2.0);
    assert math.isclose(expr.eval('ROOT(625,4)'), 5.0);
    assert expr.eval('POW(3,4)') == 81;
    assert expr.eval('INT(-1.2)') == -2;
    assert expr.eval('FIX(-1.8)') == -1;
    assert expr.eval('FLOOR(1.9)') == 1;
    assert expr.eval('CEIL(1.1)') == 2;
    assert expr.eval('ROUND(2.5)') == 3;
    assert expr.eval('ROUND(-2.5)') == -3;
    assert math.isclose(expr.eval('FRAC(-2.25)'), -0.25);
    assert expr.eval('MIN(7,3,9)') == 3;
    assert expr.eval('MAX(7,3,9)') == 9;
    assert expr.eval('CLAMP(12,0,10)') == 10;
    assert math.isclose(expr.eval('HYPOT(3,4)'), 5.0);


def test_number_theory_combinatorics_and_special_math():
    import math;
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    assert expr.eval('GCD(18,24,30)') == 6;
    assert expr.eval('LCM(6,8)') == 24;
    assert expr.eval('FACT(6)') == 720;
    assert expr.eval('COMB(6,2)') == 15;
    assert expr.eval('PERM(6,2)') == 30;
    assert math.isclose(expr.eval('GAMMA(6)'), 120.0);
    assert math.isclose(expr.eval('ERF(0)'), 0.0);
    assert expr.eval('ISFINITE(1.0)') is True;
    assert expr.eval('ISINF(1e309)') is True;


def test_bitwise_math_functions():
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    assert expr.eval('BAND(7,3)') == 3;
    assert expr.eval('BOR(4,1)') == 5;
    assert expr.eval('BXOR(5,3)') == 6;
    assert expr.eval('BNOT(0)') == -1;
    assert expr.eval('SHL(3,4)') == 48;
    assert expr.eval('SHR(48,4)') == 3;
    assert expr.eval('IDIV(17,5)') == 3;


def test_decimal_mixed_arithmetic_is_promoted_safely():
    from decimal import Decimal;
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    result = expr.eval('DECIMAL("0.1") + 0.2');
    assert result == Decimal('0.3');


def test_input_prompt_separator_semantics():
    prompts = [];
    values = iter(['Ada', '42', 'ok']);
    output = [];
    basic = BasicInterpreter(input_func=lambda prompt='': (prompts.append(prompt), next(values))[1], output_func=lambda text, end='\n': output.append(str(text) + end));
    basic.program.load_text('INPUT "texto"; A$\nINPUT "edad", B!\nINPUT C$\n');
    basic.run();
    assert prompts == ['texto? ', 'edad', '? '];
    assert basic.variables['a$'] == 'Ada';
    assert basic.variables['b!'] == 42;
    assert basic.variables['c$'] == 'ok';


def test_math_vocabulary_is_append_only_in_asc_space():
    from sumbasic.vocabulary import ASC_MODERN_CODES;
    assert ASC_MODERN_CODES[3045] == 'DIV';
    assert ASC_MODERN_CODES[3076] == 'ROUND';
    assert ASC_MODERN_CODES[3086] == 'GCD';
    assert ASC_MODERN_CODES[3114] == 'RTRIM$';
    assert ASC_MODERN_CODES[3115] == 'COMPLEX';
    assert ASC_MODERN_CODES[3127] == 'TIME$';
    assert ASC_MODERN_CODES[3130] == 'LOGBASE';



def test_log_is_base10_and_ln_is_natural():
    import math;
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    assert math.isclose(expr.eval('LOG(1000)'), 3.0);
    assert math.isclose(expr.eval('LOG10(1000)'), 3.0);
    assert math.isclose(expr.eval('LN(EXP(1))'), 1.0);
    assert math.isclose(expr.eval('LOGB(81,3)'), 4.0);
    assert math.isclose(expr.eval('LOGBASE(32,2)'), 5.0);


def test_complex_type_and_arithmetic():
    import cmath;
    import math;
    from sumbasic.expressions import ExpressionEvaluator;
    expr = ExpressionEvaluator();
    z = expr.eval('COMPLEX(3,4)');
    assert z == complex(3, 4);
    assert expr.eval('COMPLEX(3,4) + COMPLEX(1,-2)') == complex(4, 2);
    assert expr.eval('COMPLEX(3,4) * COMPLEX(1,-2)') == complex(11, -2);
    assert expr.eval('REAL(COMPLEX(3,4))') == 3.0;
    assert expr.eval('IMAG(COMPLEX(3,4))') == 4.0;
    assert expr.eval('CONJ(COMPLEX(3,4))') == complex(3, -4);
    assert expr.eval('ABS(COMPLEX(3,4))') == 5.0;
    assert expr.eval('NORM(COMPLEX(3,4))') == 25.0;
    assert math.isclose(expr.eval('PHASE(COMPLEX(0,1))'), math.pi / 2);
    assert cmath.isclose(expr.eval('SQR(COMPLEX(-1,0))'), complex(0, 1));
    assert cmath.isclose(expr.eval('EXP(COMPLEX(0,PI))'), cmath.exp(complex(0, 3.1415927)));
    assert expr.eval('ISCOMPLEX(COMPLEX(1,2))') is True;


def test_complex_declared_type_and_print_format():
    basic, out = runner('DIM Z AS COMPLEX\nZ=COMPLEX(3,4)\nPRINT Z\nPRINT STR$(CONJ(Z))\n');
    assert basic.variables['z'] == complex(3, 4);
    assert out == '3+4i\n3-4i\n';


def test_time_string_and_timer_are_deterministic_with_clock_hook():
    from datetime import datetime;
    from sumbasic.expressions import ExpressionEvaluator;
    fixed = datetime(2026, 8, 29, 1, 57, 30, 500000);
    expr = ExpressionEvaluator(now_func=lambda: fixed);
    assert expr.eval('TIME$') == '01:57:30';
    assert expr.eval('TIMER') == 7050.5;


def test_time_functions_work_in_program_source():
    from datetime import datetime;
    output = [];
    fixed = datetime(2026, 8, 29, 12, 34, 56, 250000);
    basic = BasicInterpreter(output_func=lambda text, end='\n': output.append(str(text) + end), now_func=lambda: fixed);
    basic.program.load_text('PRINT TIME$\nPRINT TIMER\n');
    basic.run();
    assert ''.join(output) == '12:34:56\n45296.25\n';


def test_pause_uses_spectrum_50hz_frames():
    sleeps = [];
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, sleep_func=lambda seconds: sleeps.append(seconds));
    basic.program.load_text('PAUSE 50\nPAUSE 25\n');
    basic.run();
    assert sleeps == [1.0, 0.5];


def test_retro_clock_example_loads_and_uses_time_font_data():
    path = Path(__file__).resolve().parents[1] / 'examples' / 'retro_clock.bas';
    text = path.read_text(encoding='utf-8');
    assert 'DIM SHARED Font$(9, 6), Colon$(6)' in text;
    assert 'T$ = TIME$' in text;
    assert 'TIMER' in text;
    assert 'BEEP .1, 0: PAUSE 45' in text;
    assert ':LOOP' in text;
    assert 'A$ = INKEY$' in text;
    assert 'GOTO LOOP' in text;
    assert 'DATA " ███ "' in text;


def test_beep_uses_spectrum_duration_pitch_and_blocks():
    import math;
    tones = [];
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, tone_func=lambda frequency, duration, blocking: tones.append((frequency, duration, blocking)));
    basic.program.load_text('BEEP 1, 0\nBEEP .5, 12\nBEEP .25, -12\n');
    basic.run();
    assert len(tones) == 3;
    assert math.isclose(tones[0][0], 261.6255653005986, rel_tol=0.0, abs_tol=1e-9);
    assert tones[0][1:] == (1.0, True);
    assert math.isclose(tones[1][0], 523.2511306011972, rel_tol=0.0, abs_tol=1e-9);
    assert tones[1][1:] == (0.5, True);
    assert math.isclose(tones[2][0], 130.8127826502993, rel_tol=0.0, abs_tol=1e-9);
    assert tones[2][1:] == (0.25, True);


def test_sound_uses_gwbasic_hz_ticks_and_is_background():
    import math;
    tones = [];
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, tone_func=lambda frequency, duration, blocking: tones.append((frequency, duration, blocking)));
    basic.program.load_text('SOUND 262, 18.2\nSOUND 440, 9.1\n');
    basic.run();
    assert tones[0][0] == 262.0;
    assert math.isclose(tones[0][1], 1.0, rel_tol=0.0, abs_tol=1e-12);
    assert tones[0][2] is False;
    assert tones[1][0] == 440.0;
    assert math.isclose(tones[1][1], 0.5, rel_tol=0.0, abs_tol=1e-12);
    assert tones[1][2] is False;


def test_sound_historical_frequency_range_is_enforced():
    from sumbasic import BasicError;
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, tone_func=lambda *args: None);
    basic.program.load_text('SOUND 36, 1\n');
    try:
        basic.run();
        assert False, 'SOUND below 37 Hz should fail';
    except BasicError:
        pass;
    basic.program.load_text('SOUND 32768, 1\n');
    try:
        basic.run();
        assert False, 'SOUND above 32767 Hz should fail';
    except BasicError:
        pass;


def test_ide_f5_runs_current_unsaved_editor_buffer(tmp_path):
    from sumbasic.ide import SumBasicIDE;
    path = tmp_path / 'program.bas';
    path.write_text('PRINT "saved"\n', encoding='utf-8');
    ide = SumBasicIDE(path=path);
    ide.editor.set_text('PRINT "unsaved"\n', modified=True);
    assert ide.keys.primary('basic.run') == 'f5';
    ide.run_program();
    assert ide.output_view.text == 'unsaved';
    assert ide.editor.modified is True;
    assert path.read_text(encoding='utf-8') == 'PRINT "saved"\n';


def test_sound_frequency_round_trips_through_spectrum_pitch_generator():
    import math;
    from sumbasic.audio import spectrum_frequency_pitch, spectrum_pitch_frequency;
    for frequency in (37.0, 130.8127826502993, 261.6255653005986, 262.0, 440.0, 523.2511306011972, 32767.0):
        pitch = spectrum_frequency_pitch(frequency);
        rebuilt = spectrum_pitch_frequency(pitch);
        assert math.isclose(rebuilt, frequency, rel_tol=1e-12, abs_tol=1e-9);


def test_system_tone_player_serializes_background_sound_requests():
    from sumbasic.audio import SystemTonePlayer;
    events = [];
    player = SystemTonePlayer();
    def fake_play(frequency, duration):
        events.append(("start", frequency));
        events.append(("end", frequency));
        return True;
    player._play_blocking = fake_play;
    player.play(220, .01, False);
    player.play(330, .01, False);
    player.play(440, .01, False);
    player.wait_for_background();
    assert events == [
        ("start", 220.0), ("end", 220.0),
        ("start", 330.0), ("end", 330.0),
        ("start", 440.0), ("end", 440.0),
    ];


def test_ide_run_screen_understands_cls_and_locate():
    from sumbasic.ide import _VirtualRunScreen;
    screen = _VirtualRunScreen();
    screen.write('old');
    screen.write('\033[2J\033[H', end='');
    screen.write('\033[4;3H', end='');
    screen.write('HI', end='');
    lines = screen.text().splitlines();
    assert lines[3] == '  HI';
    assert 'old' not in screen.text();


def test_ide_f5_toggles_nonblocking_run_stop_and_f6_switches_windows(tmp_path):
    import time;
    from sumbasic.ide import SumBasicIDE;
    path = tmp_path / 'loop.bas';
    path.write_text('PRINT "saved"\n', encoding='utf-8');
    ide = SumBasicIDE(path=path);
    ide.editor.set_text('DO\nA! = A! + 1\nLOOP\n', modified=True);
    ide.app.running = True;
    started = time.monotonic();
    ide.toggle_run();
    elapsed = time.monotonic() - started;
    assert elapsed < 0.25;
    assert ide._run_thread is not None and ide._run_thread.is_alive();
    assert ide.keys.primary('basic.run') == 'f5';
    assert ide.keys.primary('window.next') == 'f6';
    ide.app.focus.set(ide.editor);
    ide.switch_window();
    assert ide.app.focus.current is ide.output_view;
    ide.switch_window();
    assert ide.app.focus.current is ide.command_view;
    ide.switch_window();
    assert ide.app.focus.current is ide.editor;
    ide.toggle_run();
    ide._run_thread.join(timeout=2.0);
    assert not ide._run_thread.is_alive();
    ide._poll_run_state();
    assert ide.basic_interpreter.stopped_by_request is True;
    assert ide.status.text.endswith('Run stopped');
    ide.app.running = False;


def test_hybrid_numbered_label_preserves_physical_source_order():
    source = '''# Modern free-form BASIC can still use a classic numbered jump target.
PRINT "start"
GOTO 100
PRINT "wrong"
100 PRINT "target"
PRINT "done"
END
''';
    basic, out = runner(source);
    assert out == 'start\ntarget\ndone\n';
    assert basic.program.source_text() == source;


def test_sound_example_style_goto_skips_beep_block_without_looping():
    tones = [];
    output = [];
    source = '''# Two historical sound models in the same educational BASIC.
GOTO 10
PRINT "Spectrum BEEP: chromatic octave"
FOR Note! = 0 TO 12
    BEEP .08, Note!
NEXT Note!

10 PRINT "GW-BASIC SOUND: queued monophonic frequency sweep"
FOR Frequency! = 220 TO 880 STEP 55
    SOUND Frequency!, 1
NEXT Frequency!

BEEP 1, 0
SOUND 262, 18.2
END
''';
    basic = BasicInterpreter(output_func=lambda text, end="\n": output.append(str(text) + end), tone_func=lambda frequency, duration, blocking: tones.append((frequency, duration, blocking)));
    basic.program.load_text(source);
    basic.run();
    assert ''.join(output) == 'GW-BASIC SOUND: queued monophonic frequency sweep\n';
    assert len(tones) == 15;
    assert all(item[2] is False for item in tones[:13]);
    assert tones[13][2] is True;
    assert tones[14][2] is False;


def test_mixed_restore_targets_only_explicit_data_line_label():
    source = '''READ A$
PRINT A$
RESTORE 100
READ B$
PRINT B$
END
100 DATA "later"
''';
    basic, out = runner(source);
    assert out == 'later\nlater\n';


def test_named_colon_label_goto_and_colon_statement_separator():
    sleeps = [];
    tones = [];
    source = '''A! = 0
GOTO LOOP
A! = 99
:LOOP
A! = A! + 1: BEEP .1, 0: PAUSE 45
PRINT A!
END
''';
    basic = BasicInterpreter(output_func=lambda text, end="\n": None, sleep_func=lambda seconds: sleeps.append(seconds), tone_func=lambda frequency, duration, blocking: tones.append((frequency, duration, blocking)));
    basic.program.load_text(source);
    result = basic.run();
    assert result['a!'] == 1;
    assert len(tones) == 1;
    assert abs(tones[0][1] - .1) < 1e-12;
    assert tones[0][2] is True;
    assert sleeps == [.9];


def test_named_label_restore_can_target_following_data():
    source = '''RESTORE FontData
READ A$
PRINT A$
END
:FontData
DATA "retro"
''';
    basic, out = runner(source);
    assert out == 'retro\n';


def test_clock_style_inkey_loop_exits_on_q():
    keys = iter(["", "q"]);
    source = '''Count! = 0
:LOOP
Count! = Count! + 1
A$ = INKEY$: IF A$ = CHR$(27) OR A$ = "Q" OR A$ = "q" THEN END
GOTO LOOP
''';
    basic = BasicInterpreter(output_func=lambda text, end="\n": None, inkey_func=lambda: next(keys, "q"));
    basic.program.load_text(source);
    result = basic.run();
    assert result['count!'] == 2;


def test_ide_routes_q_and_escape_to_running_program_inkey(tmp_path):
    import time;
    from sumtui.events import Key, KeyEvent;
    from sumbasic.ide import SumBasicIDE;
    path = tmp_path / 'inkey.bas';
    path.write_text('PRINT "saved"\n', encoding='utf-8');
    ide = SumBasicIDE(path=path);
    ide.editor.set_text(':LOOP\nA$ = INKEY$\nIF A$ = CHR$(27) OR A$ = "Q" OR A$ = "q" THEN END\nPAUSE 1\nGOTO LOOP\n', modified=True);
    ide.app.running = True;
    original_text = ide.editor.text;
    ide.run_program();
    deadline = time.monotonic() + 1.0;
    while (ide._run_thread is None or not ide._run_thread.is_alive()) and time.monotonic() < deadline:
        time.sleep(.01);
    assert ide.app.dispatch(KeyEvent(key='q', text='q')) is True;
    ide._run_thread.join(timeout=2.0);
    assert not ide._run_thread.is_alive();
    assert ide.editor.text == original_text;
    ide._poll_run_state();
    ide.editor.set_text(':LOOP\nA$ = INKEY$\nIF A$ = CHR$(27) THEN END\nPAUSE 1\nGOTO LOOP\n', modified=True);
    ide.run_program();
    deadline = time.monotonic() + 1.0;
    while (ide._run_thread is None or not ide._run_thread.is_alive()) and time.monotonic() < deadline:
        time.sleep(.01);
    assert ide.app.dispatch(KeyEvent(key=Key.ESCAPE, text='')) is True;
    ide._run_thread.join(timeout=2.0);
    assert not ide._run_thread.is_alive();
    ide.app.running = False;



def test_terminal_inkey_reads_posix_key_without_enter():
    import os;
    if os.name == "nt":
        return;
    import pty;
    import time;
    from sumbasic.terminal_input import TerminalInput;
    master_fd, slave_fd = pty.openpty();
    stream = os.fdopen(os.dup(slave_fd), "r", buffering=1, encoding="utf-8");
    try:
        with TerminalInput(stream) as terminal:
            os.write(master_fd, b"q");
            deadline = time.monotonic() + 1.0;
            value = "";
            while not value and time.monotonic() < deadline:
                value = terminal.inkey();
                if not value:
                    time.sleep(.005);
            assert value == "q";
    finally:
        stream.close();
        os.close(master_fd);
        os.close(slave_fd);


def test_terminal_inkey_distinguishes_bare_escape_from_arrow_sequence():
    import os;
    if os.name == "nt":
        return;
    import pty;
    import time;
    from sumbasic.terminal_input import TerminalInput;
    master_fd, slave_fd = pty.openpty();
    stream = os.fdopen(os.dup(slave_fd), "r", buffering=1, encoding="utf-8");
    try:
        with TerminalInput(stream) as terminal:
            os.write(master_fd, b"\x1b[A");
            deadline = time.monotonic() + 1.0;
            value = "";
            while not value and time.monotonic() < deadline:
                value = terminal.inkey();
                if not value:
                    time.sleep(.005);
            assert value == "\x1b[A";
            os.write(master_fd, b"\x1b");
            deadline = time.monotonic() + 1.0;
            value = "";
            while not value and time.monotonic() < deadline:
                value = terminal.inkey();
                if not value:
                    time.sleep(.005);
            assert value == "\x1b";
    finally:
        stream.close();
        os.close(master_fd);
        os.close(slave_fd);


def test_stop_preserves_runtime_and_continue_resumes_after_statement():
    output = [];
    basic = BasicInterpreter(output_func=lambda text="", end="\n": output.append(str(text) + ("" if end == "" else end)));
    basic.program.load_text('A! = 1\nPRINT A!\nSTOP\nA! = A! + 1\nPRINT A!\nEND\n');
    basic.run();
    assert basic.can_continue is True;
    assert basic.stopped_by_statement is True;
    assert basic.expr.get('A!') == 1;
    assert ''.join(output) == '1\nBreak in 3\n';
    basic.continue_run();
    assert basic.can_continue is False;
    assert basic.expr.get('A!') == 2;
    assert ''.join(output) == '1\nBreak in 3\n2\n';


def test_immediate_continue_requires_prior_stop_and_resumes():
    basic, out = runner('PRINT "before"\nSTOP\nPRINT "after"\nEND\n');
    assert 'before' in out;
    assert basic.can_continue is True;
    chunks = [];
    basic.output_func = lambda text="", end="\n": chunks.append(str(text) + ("" if end == "" else end));
    basic.execute_immediate('CONTINUE');
    assert ''.join(chunks) == 'after\n';
    try:
        basic.execute_immediate('CONTINUE');
        assert False, 'CONTINUE without STOP should fail';
    except Exception as exc:
        assert 'Cannot CONTINUE' in str(exc);


def test_ide_f5_continues_after_basic_stop(tmp_path):
    from sumbasic.ide import SumBasicIDE;
    path = tmp_path / 'stop.bas';
    path.write_text('PRINT "before"\nSTOP\nPRINT "after"\nEND\n', encoding='utf-8');
    ide = SumBasicIDE(path=path);
    ide.run_program();
    assert ide.basic_interpreter.can_continue is True;
    assert 'before' in ide.output_view.text;
    ide.toggle_run();
    assert ide.basic_interpreter.can_continue is False;
    assert 'after' in ide.output_view.text;


def test_zxplay_parser_uses_spectrum_128_note_case_octaves_and_tempo():
    from sumbasic.audio import MIDDLE_C_HZ, ZXPlayParser;
    events, tempo = ZXPlayParser().parse('T120O5cC');
    assert tempo == 120;
    assert len(events) == 2;
    assert abs(events[0].frequency - MIDDLE_C_HZ) < 1e-6;
    assert abs(events[1].frequency - (MIDDLE_C_HZ * 2.0)) < 1e-6;
    assert abs(events[0].duration - .5) < 1e-12;
    assert abs(events[1].duration - .5) < 1e-12;


def test_zxplay_parser_duration_rest_accidental_and_volume():
    from sumbasic.audio import MIDDLE_C_HZ, ZXPlayParser;
    events, _ = ZXPlayParser().parse('T120O5V8N3#c&5d');
    assert len(events) == 3;
    assert abs(events[0].frequency - (MIDDLE_C_HZ * (2.0 ** (1.0 / 12.0)))) < 1e-6;
    assert abs(events[0].duration - .25) < 1e-12;
    assert abs(events[0].volume - (8.0 / 15.0)) < 1e-12;
    assert events[1].frequency is None;
    assert abs(events[1].duration - .25) < 1e-12;
    assert abs(events[2].duration - .5) < 1e-12;


def test_happy_birthday_final_phrase_has_expected_notes_and_ending():
    from sumbasic.audio import ZXPlayParser;
    events, _tempo = ZXPlayParser().parse("T120O5N3FF5ECD7C");
    assert len(events) == 6;
    frequencies = [event.frequency for event in events];
    expected_midi = [77, 77, 76, 72, 74, 72];
    expected = [440.0 * (2.0 ** ((note - 69.0) / 12.0)) for note in expected_midi];
    for actual, wanted in zip(frequencies, expected):
        assert abs(actual - wanted) < 1e-9;
    assert events[-1].duration > events[-2].duration;

def test_gwplay_parser_mml_and_background_marker():
    from sumbasic.audio import MIDDLE_C_HZ, GWPlayParser;
    events, mode = GWPlayParser().parse('MB T120 O4 L4 C');
    assert mode == 'BACKGROUND';
    assert len(events) == 2;
    assert abs(events[0].frequency - MIDDLE_C_HZ) < 1e-6;
    assert abs(sum(event.duration for event in events) - .5) < 1e-12;


def test_play_is_zxplay_alias_and_gwplay_is_separate():
    tones = [];
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, tone_func=lambda frequency, duration, blocking: tones.append((frequency, duration, blocking)));
    basic.program.load_text('PLAY "T240O5c"\nZXPLAY "T240O5d"\nGWPLAY "MF T240 O4 L4 E"\nEND\n');
    basic.run();
    basic.audio.wait_for_background();
    assert len(tones) == 3;
    assert all(item[2] is True for item in tones);
    assert tones[0][0] < tones[1][0] < tones[2][0];


def test_zxplay_channels_run_concurrently_inside_one_music_session():
    import threading;
    import time;
    from sumbasic.audio import AudioEngine;
    started = [];
    gate = threading.Event();
    lock = threading.Lock();
    def tone(frequency, duration, blocking):
        with lock: started.append(frequency);
        gate.wait(1.0);
    audio = AudioEngine(tone_func=tone);
    runner_thread = threading.Thread(target=lambda: audio.zxplay(['T240O5c', 'T240O5g'], background=False));
    runner_thread.start();
    deadline = time.monotonic() + 1.0;
    while len(started) < 2 and time.monotonic() < deadline: time.sleep(.005);
    assert len(started) == 2;
    gate.set();
    runner_thread.join(timeout=1.0);
    assert not runner_thread.is_alive();


def test_background_play_does_not_block_basic_and_audio_buses_are_independent():
    import threading;
    import time;
    from sumbasic.audio import AudioEngine;
    audio = AudioEngine();
    assert audio.beep_player is not audio.sound_player;
    assert audio.music._channel_players[0] is not audio.beep_player;
    release = threading.Event();
    started = threading.Event();
    tones = [];
    def tone(frequency, duration, blocking):
        tones.append((frequency, duration, blocking));
        started.set();
        release.wait(1.0);
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, tone_func=tone);
    basic.program.load_text('PLAY BACKGROUND "T240O5c"\nA! = 7\nEND\n');
    begin = time.monotonic();
    result = basic.run();
    assert time.monotonic() - begin < .25;
    assert result['a!'] == 7;
    assert started.wait(.5);
    release.set();
    basic.audio.wait_for_background();


def test_gwplay_explicit_background_overrides_default_foreground():
    import threading;
    import time;
    release = threading.Event();
    started = threading.Event();
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, tone_func=lambda frequency, duration, blocking: (started.set(), release.wait(1.0)));
    basic.program.load_text('GWPLAY BACKGROUND "MF T240 O4 L4 C"\nA! = 1\nEND\n');
    begin = time.monotonic();
    result = basic.run();
    assert time.monotonic() - begin < .25;
    assert result['a!'] == 1;
    assert started.wait(.5);
    release.set();
    basic.audio.wait_for_background();


def test_cli_command_and_stdin_pipeline_execution():
    import os;
    import subprocess;
    import sys;
    env = os.environ.copy();
    command = subprocess.run([sys.executable, '-m', 'sumbasic', '-c', 'PRINT "la casa roja"'], text=True, capture_output=True, env=env, check=False);
    assert command.returncode == 0;
    assert command.stdout == 'la casa roja\n';
    long_command = subprocess.run([sys.executable, '-m', 'sumbasic', '--command', 'PRINT "casa!"'], text=True, capture_output=True, env=env, check=False);
    assert long_command.returncode == 0;
    assert long_command.stdout == 'casa!\n';
    piped = subprocess.run([sys.executable, '-m', 'sumbasic'], input='PRINT "casa!"\n', text=True, capture_output=True, env=env, check=False);
    assert piped.returncode == 0;
    assert piped.stdout == 'casa!\n';


def test_zxplay_finite_phrase_repetition_matches_manual_shape():
    from sumbasic.audio import ZXPlayParser;
    events, _ = ZXPlayParser().parse('T240O5c(de)');
    notes = [event for event in events if event.frequency is not None];
    assert len(notes) == 5;
    assert abs(notes[1].frequency - notes[3].frequency) < 1e-6;
    assert abs(notes[2].frequency - notes[4].frequency) < 1e-6;


def test_a15_play_runtime_branch_executes_reported_string():
    tones = [];
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, tone_func=lambda frequency, duration, blocking: tones.append((frequency, duration, blocking)));
    basic.program.load_text('PLAY "T180O5N3cdefgabC"\nEND\n');
    basic.run();
    basic.audio.wait_for_background();
    assert len(tones) == 8;
    assert all(item[2] is True for item in tones);


def test_check_validates_statement_recognition_instead_of_only_loading():
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, tone_func=lambda *args, **kwargs: None);
    basic.program.load_text('PLAY "T180O5N3cdefgabC"\nEND\n');
    assert basic.check() is True;
    basic.program.load_text('THIS_COMMAND_DOES_NOT_EXIST 123\nEND\n');
    try:
        basic.check();
    except BasicError as exc:
        assert 'Unsupported statement' in str(exc);
    else:
        raise AssertionError('--check recognition pass accepted an unsupported statement');


def test_execute_direct_preserves_variables_and_suspended_program_context():
    output = [];
    basic = BasicInterpreter(output_func=lambda text, end="\n": output.append(str(text) + end));
    basic.program.load_text('A! = 1\nSTOP\nA! = A! + 10\nEND\n');
    basic.run();
    assert basic.can_continue is True;
    basic.execute_direct('A! = A! + 2: PRINT A!');
    assert ''.join(output).endswith('3\n');
    assert basic.can_continue is True;
    basic.continue_run();
    assert basic.variables['a!'] == 13;


def test_ide_workspace_has_code_output_command_and_window_menu(tmp_path):
    from sumbasic.ide import SumBasicIDE;
    path = tmp_path / 'hello.bas';
    path.write_text('PRINT "hello"\n', encoding='utf-8');
    ide = SumBasicIDE(path=path);
    assert [window.name for window in ide.workspace.windows] == ['output', 'command', 'code'];
    assert ide.workspace.active_window is ide.code_window;
    menu = ide._window_menu();
    labels = [item.label for item in menu.items if hasattr(item, 'label')];
    assert 'Next Window' in labels;
    assert any(label.startswith('Code') for label in labels);
    assert any(label.startswith('Output') for label in labels);
    assert any(label.startswith('Command') for label in labels);
    assert ide.close_workspace_window(ide.command_window);
    assert ide.command_window.visible is False;
    assert ide.activate_workspace_window(ide.command_window);
    assert ide.command_window.visible is True;


def test_ide_direct_command_window_runs_basic_without_saving(tmp_path):
    from sumbasic.ide import SumBasicIDE;
    path = tmp_path / 'hello.bas';
    path.write_text('PRINT "file"\n', encoding='utf-8');
    ide = SumBasicIDE(path=path);
    ide.app.running = False;
    ide._submit_direct_command('A! = 7: PRINT A!', ide.command_view);
    assert any(line == '7' for line, _role in ide.command_view.output);
    assert ide.basic_interpreter.variables['a!'] == 7;


def test_shell_command_executes_expression_and_routes_captured_output():
    commands = [];
    output = [];
    basic = BasicInterpreter(
        output_func=lambda text, end='\n': output.append(str(text) + end),
        shell_command_func=lambda command: (commands.append(command) or (0, 'one\ntwo\n')),
    );
    basic.program.load_text('CMD$ = "ls -1"\nSHELL CMD$\nEND\n');
    basic.check();
    basic.run();
    assert commands == ['ls -1'];
    assert ''.join(output) == 'one\ntwo\n';


def test_bare_shell_uses_interactive_shell_callback():
    calls = [];
    basic = BasicInterpreter(
        output_func=lambda *args, **kwargs: None,
        shell_interactive_func=lambda: (calls.append('interactive') or 0),
    );
    basic.program.load_text('SHELL\nEND\n');
    basic.check();
    basic.run();
    assert calls == ['interactive'];


def test_shell_has_separate_output_hook_for_ide_output_window():
    normal = [];
    shell = [];
    basic = BasicInterpreter(
        output_func=lambda text, end='\n': normal.append(str(text) + end),
        shell_output_func=lambda text, end='': shell.append(str(text) + end),
        shell_command_func=lambda command: (0, 'shell-result\n'),
    );
    basic.execute_direct('PRINT "direct": SHELL "echo shell-result"');
    assert ''.join(normal) == 'direct\n';
    assert ''.join(shell) == 'shell-result\n';


def test_ide_direct_shell_sends_shell_text_to_output_not_command_history(tmp_path):
    from sumbasic.ide import SumBasicIDE;
    basic = BasicInterpreter(shell_command_func=lambda command: (0, 'from-shell\n'));
    ide = SumBasicIDE(path=None, interpreter=basic);
    ide.app.running = False;
    ide._submit_direct_command('SHELL "printf from-shell"', ide.command_view);
    ide._poll_run_state();
    assert 'from-shell' in ide.output_view.text;
    assert not any('from-shell' in line for line, _role in ide.command_view.output);
    assert ide.workspace.active_window is ide.output_window;


def test_shell_check_accepts_bare_and_command_forms():
    basic = BasicInterpreter(output_func=lambda *args, **kwargs: None, shell_command_func=lambda command: (0, ''));
    basic.program.load_text('SHELL "pwd"\nSHELL\nEND\n');
    assert basic.check();


def test_ide_common_shortcuts_program_map_and_scroll_panes(tmp_path):
    from sumbasic.ide import SumBasicIDE;
    from sumtui import TextViewPane, CommandWindowPane;
    path = tmp_path / 'map.bas';
    path.write_text('PRINT "main"\nSUB Hello\nPRINT "hi"\nEND SUB\n', encoding='utf-8');
    ide = SumBasicIDE(path=path);
    assert ide.keys.primary('code.symbols') == 'f2';
    assert 'alt+p' in ide.keys.bindings_for('code.symbols');
    assert 'ctrl+q' in ide.keys.bindings_for('app.exit');
    assert 'ctrl+x' in ide.keys.bindings_for('editor.cut');
    assert 'ctrl+r' in ide.keys.bindings_for('basic.run');
    assert isinstance(ide.output_window.child, TextViewPane);
    assert isinstance(ide.command_window.child, CommandWindowPane);
    names = {item.name.strip() for item in ide.symbol_map()};
    assert 'Hello' in names;
