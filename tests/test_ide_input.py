#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import builtins;
from sumbasic.ide import SumBasicIDE;

class App:
    def __init__(self): self.called=False;
    def run_external(self, callback): self.called=True; return callback();

def test_ide_input_uses_external_terminal(monkeypatch):
    ide=SumBasicIDE.__new__(SumBasicIDE); ide.app=App();
    monkeypatch.setattr(builtins,"input",lambda prompt: "hello" if prompt=="Name? " else "bad");
    assert ide._ide_input("Name? ")=="hello";
    assert ide.app.called;
