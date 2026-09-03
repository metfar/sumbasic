#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
from sumbasic.expressions import ExpressionEvaluator;
from sumbasic.interpreter import BasicInterpreter;

def test_val_takes_first_number_only():
    ev=ExpressionEvaluator(); assert ev.eval('VAL("2+2")')==2; assert ev.eval('VAL("abc -1.5E2 xyz")')==-150;

def test_eval_uses_current_basic_environment():
    ev=ExpressionEvaluator(); ev.set("a",2); assert ev.eval('EVAL("a+2")')==4;

def test_stacked_bar_multiseries_named_form():
    basic=BasicInterpreter(); spec=basic._named_chart_spec('STACKED BAR TITLE "T" X "A","B" Y [1,2],[3,4] SERIES "one","two"')[4];
    assert spec.kind=="bar" and spec.stacked and len(spec.series)==2;

def test_bar3d_named_form():
    basic=BasicInterpreter(); spec=basic._named_chart_spec('BAR3D X "A","B" Y 1,2')[4]; assert spec.kind=="bar3d";
