#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sumui import CursorState, GraphicsCommand, GraphicsMode, TextScreen;
from sumbasic.expressions import ExpressionEvaluator;
from sumbasic.interpreter import BasicInterpreter;


class RecordingGraphics:
    def __init__(self): self.items = [];
    def __call__(self, item): self.items.append(item); return None;


def test_basic_true_false_mask_and_complex_truth_semantics():
    expr = ExpressionEvaluator();
    assert expr.eval("TRUE") == -1;
    assert expr.eval("FALSE") == 0;
    assert expr.eval("2 = 2") == -1;
    assert expr.eval("2 = 3") == 0;
    assert expr.eval('("izquierda" = "izquierda") - ("izquierda" = "derecha")') == -1;
    assert expr.eval("0x55 AND TRUE") == 0x55;
    assert expr.eval("COMPLEX(0,0) OR FALSE") == 0;
    assert expr.eval("COMPLEX(0,2) OR FALSE") == -1;


def test_basic_modern_literals_and_base_string_functions():
    expr = ExpressionEvaluator();
    assert expr.eval("&H1FF") == expr.eval("0x1FF") == 511;
    assert expr.eval("%11101") == expr.eval("0b11101") == expr.eval("BIN 11101") == 29;
    assert expr.eval("&O777") == expr.eval("0o777") == 511;
    assert expr.eval('HEX$(255,4)') == "00FF";
    assert expr.eval('OCT$(7,4)') == "0007";
    assert expr.eval('BIN$(5,8)') == "00000101";
    assert expr.eval('STR$(255)') == "255";


def test_val_tolerant_accounting_and_scientific_first_sign_wins():
    expr = ExpressionEvaluator();
    assert expr.eval('VAL("   U -1.5p6")') == -1.5;
    assert expr.eval('VAL("   LUN 1.5-6")') == -1.5;
    assert expr.eval('VAL("USD 10-")') == -10;
    assert expr.eval('VAL("+10-")') == 10;
    assert expr.eval('VAL("-10+")') == -10;
    assert expr.eval('VAL("1,234.5")') == 1234.5;
    assert expr.eval('VAL("45.3e6")') == 45300000;
    assert expr.eval('VAL("45.3e-6")') == 0.0000453;
    assert expr.eval('VAL("45.3e-6-")') == -0.0000453;
    assert expr.eval('VAL("2+2")') == 2;


def test_dynamic_cols_rows_and_basic_cursor_values():
    size = [80, 25]; states = [];
    screen = TextScreen(size_provider=lambda: tuple(size), cursor_setter=states.append);
    basic = BasicInterpreter(output_func=lambda *a, **k: None, text_screen=screen);
    assert basic.expr.eval("COLS") == 80;
    assert basic.expr.eval("ROWS") == 25;
    size[:] = [37, 19];
    assert basic.expr.eval("COLS") == 37;
    assert basic.expr.eval("ROWS") == 19;
    basic.execute_immediate("CURSOR OFF"); assert basic.expr.eval("CURSOR") == 0;
    basic.execute_immediate("CURSOR TRUE"); assert basic.expr.eval("CURSOR") == -1;
    basic.execute_immediate("CURSOR BLOCK"); assert basic.expr.eval("CURSOR") == 1;
    assert states == [CursorState.HIDDEN, CursorState.NORMAL, CursorState.BLOCK];


def test_user_rows_variable_shadows_bare_builtin_but_rows_function_stays_available():
    size = [101, 37];
    basic = BasicInterpreter(output_func=lambda *a, **k: None, text_screen=TextScreen(size_provider=lambda: tuple(size)));
    basic.execute_immediate("Rows = 7");
    assert basic.expr.eval("Rows") == 7;
    assert basic.expr.eval("ROWS()") == 37;


def test_graph_metrics_gprint_layers_and_border_pattern_commands():
    recorder = RecordingGraphics();
    basic = BasicInterpreter(output_func=lambda *a, **k: None, graphics_handler=recorder);
    source = '''DISPLAY (320,200,16,AUTO)
DEF PATTERN 3, 0xF0,0xF0,0x0F,0x0F,0b11110000,%11110000,&H0F,&O17
BORDER INK 6
BORDER PAPER 1
BORDER PATTERN 3
BORDER OFFSET 2,3
BORDER SCROLL 1,-1
GPRINT 10,20,"hello"
GPRINTF 10,40,"x=%d",7
SORT LAYERS GRAPHICS, BORDER, TEXT
CLEAR GRAPHLAYER
''';
    basic.program.load_text(source); basic.run();
    assert basic.expr.eval("GWIDTH") == 320;
    assert basic.expr.eval("GHEIGHT") == 200;
    assert basic.expr.eval("GCOLORS") == 16;
    commands = [item for item in recorder.items if isinstance(item, GraphicsCommand)];
    operations = [item.operation for item in commands];
    for expected in ("border_ink","border_paper","border_pattern","border_offset","border_scroll","text","sort_layers","clear_layer"):
        assert expected in operations;
    texts = [item for item in commands if item.operation == "text"];
    assert texts[0].arguments[:3] == (10, 20, "hello");
    assert texts[1].arguments[:3] == (10, 40, "x=7");
    layer = next(item for item in commands if item.operation == "sort_layers");
    assert layer.arguments == (("GRAPHICS", "BORDER", "TEXT"), "ASC");


def test_cls_uses_current_paper_without_resetting_border_pattern():
    recorder = RecordingGraphics();
    basic = BasicInterpreter(output_func=lambda *a, **k: None, graphics_handler=recorder);
    basic.program.load_text('DISPLAY (100,80,16,AUTO)\nPAPER 4\nBORDER 1\nCLS\n'); basic.run();
    commands = [item for item in recorder.items if isinstance(item, GraphicsCommand)];
    clear = [item for item in commands if item.operation == "clear"][-1];
    assert dict(clear.options)["color"] == 4;
    assert any(item.operation == "clear_layer" and item.arguments == ("BORDER",) for item in commands);


def test_r2021_border_width_and_graphics_pause_preserves_key():
    class Handler:
        def __init__(self): self.commands=[]; self.key="q";
        def __call__(self,item): self.commands.append(item);
        def pause(self,seconds): return True;
        def inkey(self): key,self.key=self.key,""; return key;
    handler=Handler(); basic=BasicInterpreter(graphics_handler=handler);
    basic.execute_immediate("BORDER WIDTH 24");
    assert any(getattr(item,"operation",None)=="border_width" and item.arguments==(24,) for item in handler.commands);
    basic.program.load_text('PAUSE .05\nK$ = INKEY$\nEND\n'); basic.run();
    assert basic.variables["k$"] == "q";


def test_r2022_audio_bus_volume_scales_beep_sound_and_play():
    calls = [];
    def tone(frequency, duration, blocking, volume=1.0):
        calls.append((blocking, round(float(volume), 4)));
        return True;
    basic = BasicInterpreter(output_func=lambda *a, **k: None, tone_func=tone);
    basic.execute_immediate("VOLUME BEEP 25");
    basic.execute_immediate("VOLUME SOUND 40");
    basic.execute_immediate("VOLUME PLAY 50");
    basic.execute_immediate("BEEP .01, 0");
    basic.execute_immediate("SOUND 440, .01");
    basic.execute_immediate('PLAY "T240V15O5c"');
    assert calls[0] == (True, 0.25);
    assert calls[1] == (False, 0.4);
    assert calls[2] == (True, 0.5);
    basic.execute_immediate("VOLUME 10");
    assert basic.audio.get_volume("BEEP") == 0.1;
    assert basic.audio.get_volume("SOUND") == 0.1;
    assert basic.audio.get_volume("PLAY") == 0.1;
