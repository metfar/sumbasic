#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sumbasic.expressions import ExpressionEvaluator;

def test_zero_based_shared_string_semantics():
    e=ExpressionEvaluator();
    assert e.eval('MID$("abcdef",0,1)')=="a";
    assert e.eval('INSTR("abcdef","cd")')==2;
    assert e.eval('INSTR("abcdef","xx")')==-1;
    assert e.eval('REPEAT$("ab",3)')=="ababab";
    assert e.eval('TRIM$("...hola...",".")')=="hola";
    assert e.eval('ILIKE("Montevideo","monte%")')==-1;
    assert e.eval('NUMFORMAT(5,"$ 0000.00")')=="$ 0005.00";
    assert e.eval('NUMFORMAT(5,CURRENCY)').strip().startswith("$");
    assert e.eval('BOOLFORMAT(NULL,"NO|SI|OMITIDO")')=="OMITIDO";
    assert e.eval('BOOLFORMAT(TRUE,"NO|SI|OMITIDO")')=="SI";
