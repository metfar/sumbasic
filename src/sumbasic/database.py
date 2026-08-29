#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  

class BasicDatabase:
    """BASIC-facing bridge to the xBase-compatible SumX database engine."""
    def __init__(self, path=":memory:", max_areas=10):
        try:
            from sumx.database import SumXDatabase;
        except ImportError as exc:
            raise RuntimeError("Database support requires the 'sumx' package") from exc;
        self.engine = SumXDatabase(path, max_areas=max_areas);

    @property
    def area(self): return self.engine.active_area;
    def select(self, area): return self.engine.select(area);
    def use(self, table=None, alias=None): return self.engine.use(table, alias=alias);
    def close(self): return self.engine.close();
    def recno(self): return self.engine.current_area.recno;
    def reccount(self): return self.engine.reccount();
    def go(self, record): return self.engine.go(record);
    def skip(self, count=1): return self.engine.skip(count);
    def current(self): return self.engine.current_record();
    def tables(self): return self.engine.list_tables();
