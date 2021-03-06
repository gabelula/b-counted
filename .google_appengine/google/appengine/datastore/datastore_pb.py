#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.net.proto import ProtocolBuffer
import array
import dummy_thread as thread

__pychecker__ = """maxreturns=0 maxbranches=0 no-callinit
                   unusednames=printElemNumber,debug_strs no-special"""

from google.appengine.api.api_base_pb import Integer64Proto;
from google.appengine.api.api_base_pb import StringProto;
from google.appengine.api.api_base_pb import VoidProto;
from google.appengine.datastore.entity_pb import CompositeIndex
from google.appengine.datastore.entity_pb import EntityProto
from google.appengine.datastore.entity_pb import Index
from google.appengine.datastore.entity_pb import Property
from google.appengine.datastore.entity_pb import Reference
class Transaction(ProtocolBuffer.ProtocolMessage):
  has_handle_ = 0
  handle_ = 0

  def __init__(self, contents=None):
    if contents is not None: self.MergeFromString(contents)

  def handle(self): return self.handle_

  def set_handle(self, x):
    self.has_handle_ = 1
    self.handle_ = x

  def clear_handle(self):
    self.has_handle_ = 0
    self.handle_ = 0

  def has_handle(self): return self.has_handle_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_handle()): self.set_handle(x.handle())

  def Equals(self, x):
    if x is self: return 1
    if self.has_handle_ != x.has_handle_: return 0
    if self.has_handle_ and self.handle_ != x.handle_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (not self.has_handle_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: handle not set.')
    return initialized

  def ByteSize(self):
    n = 0
    return n + 9

  def Clear(self):
    self.clear_handle()

  def OutputUnchecked(self, out):
    out.putVarInt32(9)
    out.put64(self.handle_)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 9:
        self.set_handle(d.get64())
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_handle_: res+=prefix+("handle: %s\n" % self.DebugFormatFixed64(self.handle_))
    return res

  khandle = 1

  _TEXT = (
   "ErrorCode",
   "handle",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.DOUBLE,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class Query_Filter(ProtocolBuffer.ProtocolMessage):

  LESS_THAN    =    1
  LESS_THAN_OR_EQUAL =    2
  GREATER_THAN =    3
  GREATER_THAN_OR_EQUAL =    4
  EQUAL        =    5
  IN           =    6
  EXISTS       =    7

  _Operator_NAMES = {
    1: "LESS_THAN",
    2: "LESS_THAN_OR_EQUAL",
    3: "GREATER_THAN",
    4: "GREATER_THAN_OR_EQUAL",
    5: "EQUAL",
    6: "IN",
    7: "EXISTS",
  }

  def Operator_Name(cls, x): return cls._Operator_NAMES.get(x, "")
  Operator_Name = classmethod(Operator_Name)

  has_op_ = 0
  op_ = 0

  def __init__(self, contents=None):
    self.property_ = []
    if contents is not None: self.MergeFromString(contents)

  def op(self): return self.op_

  def set_op(self, x):
    self.has_op_ = 1
    self.op_ = x

  def clear_op(self):
    self.has_op_ = 0
    self.op_ = 0

  def has_op(self): return self.has_op_

  def property_size(self): return len(self.property_)
  def property_list(self): return self.property_

  def property(self, i):
    return self.property_[i]

  def mutable_property(self, i):
    return self.property_[i]

  def add_property(self):
    x = Property()
    self.property_.append(x)
    return x

  def clear_property(self):
    self.property_ = []

  def MergeFrom(self, x):
    assert x is not self
    if (x.has_op()): self.set_op(x.op())
    for i in xrange(x.property_size()): self.add_property().CopyFrom(x.property(i))

  def Equals(self, x):
    if x is self: return 1
    if self.has_op_ != x.has_op_: return 0
    if self.has_op_ and self.op_ != x.op_: return 0
    if len(self.property_) != len(x.property_): return 0
    for e1, e2 in zip(self.property_, x.property_):
      if e1 != e2: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (not self.has_op_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: op not set.')
    for p in self.property_:
      if not p.IsInitialized(debug_strs): initialized=0
    return initialized

  def ByteSize(self):
    n = 0
    n += self.lengthVarInt64(self.op_)
    n += 1 * len(self.property_)
    for i in xrange(len(self.property_)): n += self.lengthString(self.property_[i].ByteSize())
    return n + 1

  def Clear(self):
    self.clear_op()
    self.clear_property()

  def OutputUnchecked(self, out):
    out.putVarInt32(48)
    out.putVarInt32(self.op_)
    for i in xrange(len(self.property_)):
      out.putVarInt32(114)
      out.putVarInt32(self.property_[i].ByteSize())
      self.property_[i].OutputUnchecked(out)

  def TryMerge(self, d):
    while 1:
      tt = d.getVarInt32()
      if tt == 36: break
      if tt == 48:
        self.set_op(d.getVarInt32())
        continue
      if tt == 114:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_property().TryMerge(tmp)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_op_: res+=prefix+("op: %s\n" % self.DebugFormatInt32(self.op_))
    cnt=0
    for e in self.property_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("property%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    return res

class Query_Order(ProtocolBuffer.ProtocolMessage):

  ASCENDING    =    1
  DESCENDING   =    2

  _Direction_NAMES = {
    1: "ASCENDING",
    2: "DESCENDING",
  }

  def Direction_Name(cls, x): return cls._Direction_NAMES.get(x, "")
  Direction_Name = classmethod(Direction_Name)

  has_property_ = 0
  property_ = ""
  has_direction_ = 0
  direction_ = 1

  def __init__(self, contents=None):
    if contents is not None: self.MergeFromString(contents)

  def property(self): return self.property_

  def set_property(self, x):
    self.has_property_ = 1
    self.property_ = x

  def clear_property(self):
    self.has_property_ = 0
    self.property_ = ""

  def has_property(self): return self.has_property_

  def direction(self): return self.direction_

  def set_direction(self, x):
    self.has_direction_ = 1
    self.direction_ = x

  def clear_direction(self):
    self.has_direction_ = 0
    self.direction_ = 1

  def has_direction(self): return self.has_direction_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_property()): self.set_property(x.property())
    if (x.has_direction()): self.set_direction(x.direction())

  def Equals(self, x):
    if x is self: return 1
    if self.has_property_ != x.has_property_: return 0
    if self.has_property_ and self.property_ != x.property_: return 0
    if self.has_direction_ != x.has_direction_: return 0
    if self.has_direction_ and self.direction_ != x.direction_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (not self.has_property_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: property not set.')
    return initialized

  def ByteSize(self):
    n = 0
    n += self.lengthString(len(self.property_))
    if (self.has_direction_): n += 1 + self.lengthVarInt64(self.direction_)
    return n + 1

  def Clear(self):
    self.clear_property()
    self.clear_direction()

  def OutputUnchecked(self, out):
    out.putVarInt32(82)
    out.putPrefixedString(self.property_)
    if (self.has_direction_):
      out.putVarInt32(88)
      out.putVarInt32(self.direction_)

  def TryMerge(self, d):
    while 1:
      tt = d.getVarInt32()
      if tt == 76: break
      if tt == 82:
        self.set_property(d.getPrefixedString())
        continue
      if tt == 88:
        self.set_direction(d.getVarInt32())
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_property_: res+=prefix+("property: %s\n" % self.DebugFormatString(self.property_))
    if self.has_direction_: res+=prefix+("direction: %s\n" % self.DebugFormatInt32(self.direction_))
    return res

class Query(ProtocolBuffer.ProtocolMessage):

  ORDER_FIRST  =    1
  ANCESTOR_FIRST =    2
  FILTER_FIRST =    3

  _Hint_NAMES = {
    1: "ORDER_FIRST",
    2: "ANCESTOR_FIRST",
    3: "FILTER_FIRST",
  }

  def Hint_Name(cls, x): return cls._Hint_NAMES.get(x, "")
  Hint_Name = classmethod(Hint_Name)

  has_app_ = 0
  app_ = ""
  has_kind_ = 0
  kind_ = ""
  has_ancestor_ = 0
  ancestor_ = None
  has_search_query_ = 0
  search_query_ = ""
  has_hint_ = 0
  hint_ = 0
  has_offset_ = 0
  offset_ = 0
  has_limit_ = 0
  limit_ = 0
  has_require_perfect_plan_ = 0
  require_perfect_plan_ = 0

  def __init__(self, contents=None):
    self.filter_ = []
    self.order_ = []
    self.composite_index_ = []
    self.lazy_init_lock_ = thread.allocate_lock()
    if contents is not None: self.MergeFromString(contents)

  def app(self): return self.app_

  def set_app(self, x):
    self.has_app_ = 1
    self.app_ = x

  def clear_app(self):
    self.has_app_ = 0
    self.app_ = ""

  def has_app(self): return self.has_app_

  def kind(self): return self.kind_

  def set_kind(self, x):
    self.has_kind_ = 1
    self.kind_ = x

  def clear_kind(self):
    self.has_kind_ = 0
    self.kind_ = ""

  def has_kind(self): return self.has_kind_

  def ancestor(self):
    if self.ancestor_ is None:
      self.lazy_init_lock_.acquire()
      try:
        if self.ancestor_ is None: self.ancestor_ = Reference()
      finally:
        self.lazy_init_lock_.release()
    return self.ancestor_

  def mutable_ancestor(self): self.has_ancestor_ = 1; return self.ancestor()

  def clear_ancestor(self):
    self.has_ancestor_ = 0;
    if self.ancestor_ is not None: self.ancestor_.Clear()

  def has_ancestor(self): return self.has_ancestor_

  def filter_size(self): return len(self.filter_)
  def filter_list(self): return self.filter_

  def filter(self, i):
    return self.filter_[i]

  def mutable_filter(self, i):
    return self.filter_[i]

  def add_filter(self):
    x = Query_Filter()
    self.filter_.append(x)
    return x

  def clear_filter(self):
    self.filter_ = []
  def search_query(self): return self.search_query_

  def set_search_query(self, x):
    self.has_search_query_ = 1
    self.search_query_ = x

  def clear_search_query(self):
    self.has_search_query_ = 0
    self.search_query_ = ""

  def has_search_query(self): return self.has_search_query_

  def order_size(self): return len(self.order_)
  def order_list(self): return self.order_

  def order(self, i):
    return self.order_[i]

  def mutable_order(self, i):
    return self.order_[i]

  def add_order(self):
    x = Query_Order()
    self.order_.append(x)
    return x

  def clear_order(self):
    self.order_ = []
  def hint(self): return self.hint_

  def set_hint(self, x):
    self.has_hint_ = 1
    self.hint_ = x

  def clear_hint(self):
    self.has_hint_ = 0
    self.hint_ = 0

  def has_hint(self): return self.has_hint_

  def offset(self): return self.offset_

  def set_offset(self, x):
    self.has_offset_ = 1
    self.offset_ = x

  def clear_offset(self):
    self.has_offset_ = 0
    self.offset_ = 0

  def has_offset(self): return self.has_offset_

  def limit(self): return self.limit_

  def set_limit(self, x):
    self.has_limit_ = 1
    self.limit_ = x

  def clear_limit(self):
    self.has_limit_ = 0
    self.limit_ = 0

  def has_limit(self): return self.has_limit_

  def composite_index_size(self): return len(self.composite_index_)
  def composite_index_list(self): return self.composite_index_

  def composite_index(self, i):
    return self.composite_index_[i]

  def mutable_composite_index(self, i):
    return self.composite_index_[i]

  def add_composite_index(self):
    x = CompositeIndex()
    self.composite_index_.append(x)
    return x

  def clear_composite_index(self):
    self.composite_index_ = []
  def require_perfect_plan(self): return self.require_perfect_plan_

  def set_require_perfect_plan(self, x):
    self.has_require_perfect_plan_ = 1
    self.require_perfect_plan_ = x

  def clear_require_perfect_plan(self):
    self.has_require_perfect_plan_ = 0
    self.require_perfect_plan_ = 0

  def has_require_perfect_plan(self): return self.has_require_perfect_plan_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_app()): self.set_app(x.app())
    if (x.has_kind()): self.set_kind(x.kind())
    if (x.has_ancestor()): self.mutable_ancestor().MergeFrom(x.ancestor())
    for i in xrange(x.filter_size()): self.add_filter().CopyFrom(x.filter(i))
    if (x.has_search_query()): self.set_search_query(x.search_query())
    for i in xrange(x.order_size()): self.add_order().CopyFrom(x.order(i))
    if (x.has_hint()): self.set_hint(x.hint())
    if (x.has_offset()): self.set_offset(x.offset())
    if (x.has_limit()): self.set_limit(x.limit())
    for i in xrange(x.composite_index_size()): self.add_composite_index().CopyFrom(x.composite_index(i))
    if (x.has_require_perfect_plan()): self.set_require_perfect_plan(x.require_perfect_plan())

  def Equals(self, x):
    if x is self: return 1
    if self.has_app_ != x.has_app_: return 0
    if self.has_app_ and self.app_ != x.app_: return 0
    if self.has_kind_ != x.has_kind_: return 0
    if self.has_kind_ and self.kind_ != x.kind_: return 0
    if self.has_ancestor_ != x.has_ancestor_: return 0
    if self.has_ancestor_ and self.ancestor_ != x.ancestor_: return 0
    if len(self.filter_) != len(x.filter_): return 0
    for e1, e2 in zip(self.filter_, x.filter_):
      if e1 != e2: return 0
    if self.has_search_query_ != x.has_search_query_: return 0
    if self.has_search_query_ and self.search_query_ != x.search_query_: return 0
    if len(self.order_) != len(x.order_): return 0
    for e1, e2 in zip(self.order_, x.order_):
      if e1 != e2: return 0
    if self.has_hint_ != x.has_hint_: return 0
    if self.has_hint_ and self.hint_ != x.hint_: return 0
    if self.has_offset_ != x.has_offset_: return 0
    if self.has_offset_ and self.offset_ != x.offset_: return 0
    if self.has_limit_ != x.has_limit_: return 0
    if self.has_limit_ and self.limit_ != x.limit_: return 0
    if len(self.composite_index_) != len(x.composite_index_): return 0
    for e1, e2 in zip(self.composite_index_, x.composite_index_):
      if e1 != e2: return 0
    if self.has_require_perfect_plan_ != x.has_require_perfect_plan_: return 0
    if self.has_require_perfect_plan_ and self.require_perfect_plan_ != x.require_perfect_plan_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (not self.has_app_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: app not set.')
    if (self.has_ancestor_ and not self.ancestor_.IsInitialized(debug_strs)): initialized = 0
    for p in self.filter_:
      if not p.IsInitialized(debug_strs): initialized=0
    for p in self.order_:
      if not p.IsInitialized(debug_strs): initialized=0
    for p in self.composite_index_:
      if not p.IsInitialized(debug_strs): initialized=0
    return initialized

  def ByteSize(self):
    n = 0
    n += self.lengthString(len(self.app_))
    if (self.has_kind_): n += 1 + self.lengthString(len(self.kind_))
    if (self.has_ancestor_): n += 2 + self.lengthString(self.ancestor_.ByteSize())
    n += 2 * len(self.filter_)
    for i in xrange(len(self.filter_)): n += self.filter_[i].ByteSize()
    if (self.has_search_query_): n += 1 + self.lengthString(len(self.search_query_))
    n += 2 * len(self.order_)
    for i in xrange(len(self.order_)): n += self.order_[i].ByteSize()
    if (self.has_hint_): n += 2 + self.lengthVarInt64(self.hint_)
    if (self.has_offset_): n += 1 + self.lengthVarInt64(self.offset_)
    if (self.has_limit_): n += 2 + self.lengthVarInt64(self.limit_)
    n += 2 * len(self.composite_index_)
    for i in xrange(len(self.composite_index_)): n += self.lengthString(self.composite_index_[i].ByteSize())
    if (self.has_require_perfect_plan_): n += 3
    return n + 1

  def Clear(self):
    self.clear_app()
    self.clear_kind()
    self.clear_ancestor()
    self.clear_filter()
    self.clear_search_query()
    self.clear_order()
    self.clear_hint()
    self.clear_offset()
    self.clear_limit()
    self.clear_composite_index()
    self.clear_require_perfect_plan()

  def OutputUnchecked(self, out):
    out.putVarInt32(10)
    out.putPrefixedString(self.app_)
    if (self.has_kind_):
      out.putVarInt32(26)
      out.putPrefixedString(self.kind_)
    for i in xrange(len(self.filter_)):
      out.putVarInt32(35)
      self.filter_[i].OutputUnchecked(out)
      out.putVarInt32(36)
    if (self.has_search_query_):
      out.putVarInt32(66)
      out.putPrefixedString(self.search_query_)
    for i in xrange(len(self.order_)):
      out.putVarInt32(75)
      self.order_[i].OutputUnchecked(out)
      out.putVarInt32(76)
    if (self.has_offset_):
      out.putVarInt32(96)
      out.putVarInt32(self.offset_)
    if (self.has_limit_):
      out.putVarInt32(128)
      out.putVarInt32(self.limit_)
    if (self.has_ancestor_):
      out.putVarInt32(138)
      out.putVarInt32(self.ancestor_.ByteSize())
      self.ancestor_.OutputUnchecked(out)
    if (self.has_hint_):
      out.putVarInt32(144)
      out.putVarInt32(self.hint_)
    for i in xrange(len(self.composite_index_)):
      out.putVarInt32(154)
      out.putVarInt32(self.composite_index_[i].ByteSize())
      self.composite_index_[i].OutputUnchecked(out)
    if (self.has_require_perfect_plan_):
      out.putVarInt32(160)
      out.putBoolean(self.require_perfect_plan_)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        self.set_app(d.getPrefixedString())
        continue
      if tt == 26:
        self.set_kind(d.getPrefixedString())
        continue
      if tt == 35:
        self.add_filter().TryMerge(d)
        continue
      if tt == 66:
        self.set_search_query(d.getPrefixedString())
        continue
      if tt == 75:
        self.add_order().TryMerge(d)
        continue
      if tt == 96:
        self.set_offset(d.getVarInt32())
        continue
      if tt == 128:
        self.set_limit(d.getVarInt32())
        continue
      if tt == 138:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.mutable_ancestor().TryMerge(tmp)
        continue
      if tt == 144:
        self.set_hint(d.getVarInt32())
        continue
      if tt == 154:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_composite_index().TryMerge(tmp)
        continue
      if tt == 160:
        self.set_require_perfect_plan(d.getBoolean())
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_app_: res+=prefix+("app: %s\n" % self.DebugFormatString(self.app_))
    if self.has_kind_: res+=prefix+("kind: %s\n" % self.DebugFormatString(self.kind_))
    if self.has_ancestor_:
      res+=prefix+"ancestor <\n"
      res+=self.ancestor_.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
    cnt=0
    for e in self.filter_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("Filter%s {\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+"}\n"
      cnt+=1
    if self.has_search_query_: res+=prefix+("search_query: %s\n" % self.DebugFormatString(self.search_query_))
    cnt=0
    for e in self.order_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("Order%s {\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+"}\n"
      cnt+=1
    if self.has_hint_: res+=prefix+("hint: %s\n" % self.DebugFormatInt32(self.hint_))
    if self.has_offset_: res+=prefix+("offset: %s\n" % self.DebugFormatInt32(self.offset_))
    if self.has_limit_: res+=prefix+("limit: %s\n" % self.DebugFormatInt32(self.limit_))
    cnt=0
    for e in self.composite_index_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("composite_index%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    if self.has_require_perfect_plan_: res+=prefix+("require_perfect_plan: %s\n" % self.DebugFormatBool(self.require_perfect_plan_))
    return res

  kapp = 1
  kkind = 3
  kancestor = 17
  kFilterGroup = 4
  kFilterop = 6
  kFilterproperty = 14
  ksearch_query = 8
  kOrderGroup = 9
  kOrderproperty = 10
  kOrderdirection = 11
  khint = 18
  koffset = 12
  klimit = 16
  kcomposite_index = 19
  krequire_perfect_plan = 20

  _TEXT = (
   "ErrorCode",
   "app",
   None,
   "kind",
   "Filter",
   None,
   "op",
   None,
   "search_query",
   "Order",
   "property",
   "direction",
   "offset",
   None,
   "property",
   None,
   "limit",
   "ancestor",
   "hint",
   "composite_index",
   "require_perfect_plan",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.STARTGROUP,

   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.NUMERIC,

   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.STARTGROUP,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.NUMERIC,

   ProtocolBuffer.Encoder.NUMERIC,

   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.NUMERIC,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.NUMERIC,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.NUMERIC,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class QueryExplanation(ProtocolBuffer.ProtocolMessage):
  has_native_ancestor_ = 0
  native_ancestor_ = 0
  has_native_offset_ = 0
  native_offset_ = 0
  has_native_limit_ = 0
  native_limit_ = 0

  def __init__(self, contents=None):
    self.native_index_ = []
    if contents is not None: self.MergeFromString(contents)

  def native_ancestor(self): return self.native_ancestor_

  def set_native_ancestor(self, x):
    self.has_native_ancestor_ = 1
    self.native_ancestor_ = x

  def clear_native_ancestor(self):
    self.has_native_ancestor_ = 0
    self.native_ancestor_ = 0

  def has_native_ancestor(self): return self.has_native_ancestor_

  def native_index_size(self): return len(self.native_index_)
  def native_index_list(self): return self.native_index_

  def native_index(self, i):
    return self.native_index_[i]

  def mutable_native_index(self, i):
    return self.native_index_[i]

  def add_native_index(self):
    x = Index()
    self.native_index_.append(x)
    return x

  def clear_native_index(self):
    self.native_index_ = []
  def native_offset(self): return self.native_offset_

  def set_native_offset(self, x):
    self.has_native_offset_ = 1
    self.native_offset_ = x

  def clear_native_offset(self):
    self.has_native_offset_ = 0
    self.native_offset_ = 0

  def has_native_offset(self): return self.has_native_offset_

  def native_limit(self): return self.native_limit_

  def set_native_limit(self, x):
    self.has_native_limit_ = 1
    self.native_limit_ = x

  def clear_native_limit(self):
    self.has_native_limit_ = 0
    self.native_limit_ = 0

  def has_native_limit(self): return self.has_native_limit_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_native_ancestor()): self.set_native_ancestor(x.native_ancestor())
    for i in xrange(x.native_index_size()): self.add_native_index().CopyFrom(x.native_index(i))
    if (x.has_native_offset()): self.set_native_offset(x.native_offset())
    if (x.has_native_limit()): self.set_native_limit(x.native_limit())

  def Equals(self, x):
    if x is self: return 1
    if self.has_native_ancestor_ != x.has_native_ancestor_: return 0
    if self.has_native_ancestor_ and self.native_ancestor_ != x.native_ancestor_: return 0
    if len(self.native_index_) != len(x.native_index_): return 0
    for e1, e2 in zip(self.native_index_, x.native_index_):
      if e1 != e2: return 0
    if self.has_native_offset_ != x.has_native_offset_: return 0
    if self.has_native_offset_ and self.native_offset_ != x.native_offset_: return 0
    if self.has_native_limit_ != x.has_native_limit_: return 0
    if self.has_native_limit_ and self.native_limit_ != x.native_limit_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    for p in self.native_index_:
      if not p.IsInitialized(debug_strs): initialized=0
    return initialized

  def ByteSize(self):
    n = 0
    if (self.has_native_ancestor_): n += 2
    n += 1 * len(self.native_index_)
    for i in xrange(len(self.native_index_)): n += self.lengthString(self.native_index_[i].ByteSize())
    if (self.has_native_offset_): n += 1 + self.lengthVarInt64(self.native_offset_)
    if (self.has_native_limit_): n += 1 + self.lengthVarInt64(self.native_limit_)
    return n + 0

  def Clear(self):
    self.clear_native_ancestor()
    self.clear_native_index()
    self.clear_native_offset()
    self.clear_native_limit()

  def OutputUnchecked(self, out):
    if (self.has_native_ancestor_):
      out.putVarInt32(8)
      out.putBoolean(self.native_ancestor_)
    for i in xrange(len(self.native_index_)):
      out.putVarInt32(18)
      out.putVarInt32(self.native_index_[i].ByteSize())
      self.native_index_[i].OutputUnchecked(out)
    if (self.has_native_offset_):
      out.putVarInt32(24)
      out.putVarInt32(self.native_offset_)
    if (self.has_native_limit_):
      out.putVarInt32(32)
      out.putVarInt32(self.native_limit_)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 8:
        self.set_native_ancestor(d.getBoolean())
        continue
      if tt == 18:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_native_index().TryMerge(tmp)
        continue
      if tt == 24:
        self.set_native_offset(d.getVarInt32())
        continue
      if tt == 32:
        self.set_native_limit(d.getVarInt32())
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_native_ancestor_: res+=prefix+("native_ancestor: %s\n" % self.DebugFormatBool(self.native_ancestor_))
    cnt=0
    for e in self.native_index_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("native_index%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    if self.has_native_offset_: res+=prefix+("native_offset: %s\n" % self.DebugFormatInt32(self.native_offset_))
    if self.has_native_limit_: res+=prefix+("native_limit: %s\n" % self.DebugFormatInt32(self.native_limit_))
    return res

  knative_ancestor = 1
  knative_index = 2
  knative_offset = 3
  knative_limit = 4

  _TEXT = (
   "ErrorCode",
   "native_ancestor",
   "native_index",
   "native_offset",
   "native_limit",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.NUMERIC,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.NUMERIC,

   ProtocolBuffer.Encoder.NUMERIC,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class Cursor(ProtocolBuffer.ProtocolMessage):
  has_cursor_ = 0
  cursor_ = 0

  def __init__(self, contents=None):
    if contents is not None: self.MergeFromString(contents)

  def cursor(self): return self.cursor_

  def set_cursor(self, x):
    self.has_cursor_ = 1
    self.cursor_ = x

  def clear_cursor(self):
    self.has_cursor_ = 0
    self.cursor_ = 0

  def has_cursor(self): return self.has_cursor_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_cursor()): self.set_cursor(x.cursor())

  def Equals(self, x):
    if x is self: return 1
    if self.has_cursor_ != x.has_cursor_: return 0
    if self.has_cursor_ and self.cursor_ != x.cursor_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (not self.has_cursor_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: cursor not set.')
    return initialized

  def ByteSize(self):
    n = 0
    return n + 9

  def Clear(self):
    self.clear_cursor()

  def OutputUnchecked(self, out):
    out.putVarInt32(9)
    out.put64(self.cursor_)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 9:
        self.set_cursor(d.get64())
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_cursor_: res+=prefix+("cursor: %s\n" % self.DebugFormatFixed64(self.cursor_))
    return res

  kcursor = 1

  _TEXT = (
   "ErrorCode",
   "cursor",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.DOUBLE,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class Error(ProtocolBuffer.ProtocolMessage):

  BAD_REQUEST  =    1
  CONCURRENT_TRANSACTION =    2
  INTERNAL_ERROR =    3
  NEED_INDEX   =    4
  TIMEOUT      =    5

  _ErrorCode_NAMES = {
    1: "BAD_REQUEST",
    2: "CONCURRENT_TRANSACTION",
    3: "INTERNAL_ERROR",
    4: "NEED_INDEX",
    5: "TIMEOUT",
  }

  def ErrorCode_Name(cls, x): return cls._ErrorCode_NAMES.get(x, "")
  ErrorCode_Name = classmethod(ErrorCode_Name)


  def __init__(self, contents=None):
    pass
    if contents is not None: self.MergeFromString(contents)


  def MergeFrom(self, x):
    assert x is not self

  def Equals(self, x):
    if x is self: return 1
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    return initialized

  def ByteSize(self):
    n = 0
    return n + 0

  def Clear(self):
    pass

  def OutputUnchecked(self, out):
    pass

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    return res


  _TEXT = (
   "ErrorCode",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class GetRequest(ProtocolBuffer.ProtocolMessage):
  has_transaction_ = 0
  transaction_ = None

  def __init__(self, contents=None):
    self.key_ = []
    self.lazy_init_lock_ = thread.allocate_lock()
    if contents is not None: self.MergeFromString(contents)

  def key_size(self): return len(self.key_)
  def key_list(self): return self.key_

  def key(self, i):
    return self.key_[i]

  def mutable_key(self, i):
    return self.key_[i]

  def add_key(self):
    x = Reference()
    self.key_.append(x)
    return x

  def clear_key(self):
    self.key_ = []
  def transaction(self):
    if self.transaction_ is None:
      self.lazy_init_lock_.acquire()
      try:
        if self.transaction_ is None: self.transaction_ = Transaction()
      finally:
        self.lazy_init_lock_.release()
    return self.transaction_

  def mutable_transaction(self): self.has_transaction_ = 1; return self.transaction()

  def clear_transaction(self):
    self.has_transaction_ = 0;
    if self.transaction_ is not None: self.transaction_.Clear()

  def has_transaction(self): return self.has_transaction_


  def MergeFrom(self, x):
    assert x is not self
    for i in xrange(x.key_size()): self.add_key().CopyFrom(x.key(i))
    if (x.has_transaction()): self.mutable_transaction().MergeFrom(x.transaction())

  def Equals(self, x):
    if x is self: return 1
    if len(self.key_) != len(x.key_): return 0
    for e1, e2 in zip(self.key_, x.key_):
      if e1 != e2: return 0
    if self.has_transaction_ != x.has_transaction_: return 0
    if self.has_transaction_ and self.transaction_ != x.transaction_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    for p in self.key_:
      if not p.IsInitialized(debug_strs): initialized=0
    if (self.has_transaction_ and not self.transaction_.IsInitialized(debug_strs)): initialized = 0
    return initialized

  def ByteSize(self):
    n = 0
    n += 1 * len(self.key_)
    for i in xrange(len(self.key_)): n += self.lengthString(self.key_[i].ByteSize())
    if (self.has_transaction_): n += 1 + self.lengthString(self.transaction_.ByteSize())
    return n + 0

  def Clear(self):
    self.clear_key()
    self.clear_transaction()

  def OutputUnchecked(self, out):
    for i in xrange(len(self.key_)):
      out.putVarInt32(10)
      out.putVarInt32(self.key_[i].ByteSize())
      self.key_[i].OutputUnchecked(out)
    if (self.has_transaction_):
      out.putVarInt32(18)
      out.putVarInt32(self.transaction_.ByteSize())
      self.transaction_.OutputUnchecked(out)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_key().TryMerge(tmp)
        continue
      if tt == 18:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.mutable_transaction().TryMerge(tmp)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    cnt=0
    for e in self.key_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("key%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    if self.has_transaction_:
      res+=prefix+"transaction <\n"
      res+=self.transaction_.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
    return res

  kkey = 1
  ktransaction = 2

  _TEXT = (
   "ErrorCode",
   "key",
   "transaction",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.STRING,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class GetResponse_Entity(ProtocolBuffer.ProtocolMessage):
  has_entity_ = 0
  entity_ = None

  def __init__(self, contents=None):
    self.lazy_init_lock_ = thread.allocate_lock()
    if contents is not None: self.MergeFromString(contents)

  def entity(self):
    if self.entity_ is None:
      self.lazy_init_lock_.acquire()
      try:
        if self.entity_ is None: self.entity_ = EntityProto()
      finally:
        self.lazy_init_lock_.release()
    return self.entity_

  def mutable_entity(self): self.has_entity_ = 1; return self.entity()

  def clear_entity(self):
    self.has_entity_ = 0;
    if self.entity_ is not None: self.entity_.Clear()

  def has_entity(self): return self.has_entity_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_entity()): self.mutable_entity().MergeFrom(x.entity())

  def Equals(self, x):
    if x is self: return 1
    if self.has_entity_ != x.has_entity_: return 0
    if self.has_entity_ and self.entity_ != x.entity_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (self.has_entity_ and not self.entity_.IsInitialized(debug_strs)): initialized = 0
    return initialized

  def ByteSize(self):
    n = 0
    if (self.has_entity_): n += 1 + self.lengthString(self.entity_.ByteSize())
    return n + 0

  def Clear(self):
    self.clear_entity()

  def OutputUnchecked(self, out):
    if (self.has_entity_):
      out.putVarInt32(18)
      out.putVarInt32(self.entity_.ByteSize())
      self.entity_.OutputUnchecked(out)

  def TryMerge(self, d):
    while 1:
      tt = d.getVarInt32()
      if tt == 12: break
      if tt == 18:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.mutable_entity().TryMerge(tmp)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_entity_:
      res+=prefix+"entity <\n"
      res+=self.entity_.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
    return res

class GetResponse(ProtocolBuffer.ProtocolMessage):

  def __init__(self, contents=None):
    self.entity_ = []
    if contents is not None: self.MergeFromString(contents)

  def entity_size(self): return len(self.entity_)
  def entity_list(self): return self.entity_

  def entity(self, i):
    return self.entity_[i]

  def mutable_entity(self, i):
    return self.entity_[i]

  def add_entity(self):
    x = GetResponse_Entity()
    self.entity_.append(x)
    return x

  def clear_entity(self):
    self.entity_ = []

  def MergeFrom(self, x):
    assert x is not self
    for i in xrange(x.entity_size()): self.add_entity().CopyFrom(x.entity(i))

  def Equals(self, x):
    if x is self: return 1
    if len(self.entity_) != len(x.entity_): return 0
    for e1, e2 in zip(self.entity_, x.entity_):
      if e1 != e2: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    for p in self.entity_:
      if not p.IsInitialized(debug_strs): initialized=0
    return initialized

  def ByteSize(self):
    n = 0
    n += 2 * len(self.entity_)
    for i in xrange(len(self.entity_)): n += self.entity_[i].ByteSize()
    return n + 0

  def Clear(self):
    self.clear_entity()

  def OutputUnchecked(self, out):
    for i in xrange(len(self.entity_)):
      out.putVarInt32(11)
      self.entity_[i].OutputUnchecked(out)
      out.putVarInt32(12)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 11:
        self.add_entity().TryMerge(d)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    cnt=0
    for e in self.entity_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("Entity%s {\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+"}\n"
      cnt+=1
    return res

  kEntityGroup = 1
  kEntityentity = 2

  _TEXT = (
   "ErrorCode",
   "Entity",
   "entity",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STARTGROUP,

   ProtocolBuffer.Encoder.STRING,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class PutRequest(ProtocolBuffer.ProtocolMessage):
  has_transaction_ = 0
  transaction_ = None

  def __init__(self, contents=None):
    self.entity_ = []
    self.composite_index_ = []
    self.lazy_init_lock_ = thread.allocate_lock()
    if contents is not None: self.MergeFromString(contents)

  def entity_size(self): return len(self.entity_)
  def entity_list(self): return self.entity_

  def entity(self, i):
    return self.entity_[i]

  def mutable_entity(self, i):
    return self.entity_[i]

  def add_entity(self):
    x = EntityProto()
    self.entity_.append(x)
    return x

  def clear_entity(self):
    self.entity_ = []
  def transaction(self):
    if self.transaction_ is None:
      self.lazy_init_lock_.acquire()
      try:
        if self.transaction_ is None: self.transaction_ = Transaction()
      finally:
        self.lazy_init_lock_.release()
    return self.transaction_

  def mutable_transaction(self): self.has_transaction_ = 1; return self.transaction()

  def clear_transaction(self):
    self.has_transaction_ = 0;
    if self.transaction_ is not None: self.transaction_.Clear()

  def has_transaction(self): return self.has_transaction_

  def composite_index_size(self): return len(self.composite_index_)
  def composite_index_list(self): return self.composite_index_

  def composite_index(self, i):
    return self.composite_index_[i]

  def mutable_composite_index(self, i):
    return self.composite_index_[i]

  def add_composite_index(self):
    x = CompositeIndex()
    self.composite_index_.append(x)
    return x

  def clear_composite_index(self):
    self.composite_index_ = []

  def MergeFrom(self, x):
    assert x is not self
    for i in xrange(x.entity_size()): self.add_entity().CopyFrom(x.entity(i))
    if (x.has_transaction()): self.mutable_transaction().MergeFrom(x.transaction())
    for i in xrange(x.composite_index_size()): self.add_composite_index().CopyFrom(x.composite_index(i))

  def Equals(self, x):
    if x is self: return 1
    if len(self.entity_) != len(x.entity_): return 0
    for e1, e2 in zip(self.entity_, x.entity_):
      if e1 != e2: return 0
    if self.has_transaction_ != x.has_transaction_: return 0
    if self.has_transaction_ and self.transaction_ != x.transaction_: return 0
    if len(self.composite_index_) != len(x.composite_index_): return 0
    for e1, e2 in zip(self.composite_index_, x.composite_index_):
      if e1 != e2: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    for p in self.entity_:
      if not p.IsInitialized(debug_strs): initialized=0
    if (self.has_transaction_ and not self.transaction_.IsInitialized(debug_strs)): initialized = 0
    for p in self.composite_index_:
      if not p.IsInitialized(debug_strs): initialized=0
    return initialized

  def ByteSize(self):
    n = 0
    n += 1 * len(self.entity_)
    for i in xrange(len(self.entity_)): n += self.lengthString(self.entity_[i].ByteSize())
    if (self.has_transaction_): n += 1 + self.lengthString(self.transaction_.ByteSize())
    n += 1 * len(self.composite_index_)
    for i in xrange(len(self.composite_index_)): n += self.lengthString(self.composite_index_[i].ByteSize())
    return n + 0

  def Clear(self):
    self.clear_entity()
    self.clear_transaction()
    self.clear_composite_index()

  def OutputUnchecked(self, out):
    for i in xrange(len(self.entity_)):
      out.putVarInt32(10)
      out.putVarInt32(self.entity_[i].ByteSize())
      self.entity_[i].OutputUnchecked(out)
    if (self.has_transaction_):
      out.putVarInt32(18)
      out.putVarInt32(self.transaction_.ByteSize())
      self.transaction_.OutputUnchecked(out)
    for i in xrange(len(self.composite_index_)):
      out.putVarInt32(26)
      out.putVarInt32(self.composite_index_[i].ByteSize())
      self.composite_index_[i].OutputUnchecked(out)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_entity().TryMerge(tmp)
        continue
      if tt == 18:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.mutable_transaction().TryMerge(tmp)
        continue
      if tt == 26:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_composite_index().TryMerge(tmp)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    cnt=0
    for e in self.entity_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("entity%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    if self.has_transaction_:
      res+=prefix+"transaction <\n"
      res+=self.transaction_.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
    cnt=0
    for e in self.composite_index_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("composite_index%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    return res

  kentity = 1
  ktransaction = 2
  kcomposite_index = 3

  _TEXT = (
   "ErrorCode",
   "entity",
   "transaction",
   "composite_index",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.STRING,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class PutResponse(ProtocolBuffer.ProtocolMessage):

  def __init__(self, contents=None):
    self.key_ = []
    if contents is not None: self.MergeFromString(contents)

  def key_size(self): return len(self.key_)
  def key_list(self): return self.key_

  def key(self, i):
    return self.key_[i]

  def mutable_key(self, i):
    return self.key_[i]

  def add_key(self):
    x = Reference()
    self.key_.append(x)
    return x

  def clear_key(self):
    self.key_ = []

  def MergeFrom(self, x):
    assert x is not self
    for i in xrange(x.key_size()): self.add_key().CopyFrom(x.key(i))

  def Equals(self, x):
    if x is self: return 1
    if len(self.key_) != len(x.key_): return 0
    for e1, e2 in zip(self.key_, x.key_):
      if e1 != e2: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    for p in self.key_:
      if not p.IsInitialized(debug_strs): initialized=0
    return initialized

  def ByteSize(self):
    n = 0
    n += 1 * len(self.key_)
    for i in xrange(len(self.key_)): n += self.lengthString(self.key_[i].ByteSize())
    return n + 0

  def Clear(self):
    self.clear_key()

  def OutputUnchecked(self, out):
    for i in xrange(len(self.key_)):
      out.putVarInt32(10)
      out.putVarInt32(self.key_[i].ByteSize())
      self.key_[i].OutputUnchecked(out)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_key().TryMerge(tmp)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    cnt=0
    for e in self.key_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("key%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    return res

  kkey = 1

  _TEXT = (
   "ErrorCode",
   "key",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STRING,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class DeleteRequest(ProtocolBuffer.ProtocolMessage):
  has_transaction_ = 0
  transaction_ = None

  def __init__(self, contents=None):
    self.key_ = []
    self.lazy_init_lock_ = thread.allocate_lock()
    if contents is not None: self.MergeFromString(contents)

  def key_size(self): return len(self.key_)
  def key_list(self): return self.key_

  def key(self, i):
    return self.key_[i]

  def mutable_key(self, i):
    return self.key_[i]

  def add_key(self):
    x = Reference()
    self.key_.append(x)
    return x

  def clear_key(self):
    self.key_ = []
  def transaction(self):
    if self.transaction_ is None:
      self.lazy_init_lock_.acquire()
      try:
        if self.transaction_ is None: self.transaction_ = Transaction()
      finally:
        self.lazy_init_lock_.release()
    return self.transaction_

  def mutable_transaction(self): self.has_transaction_ = 1; return self.transaction()

  def clear_transaction(self):
    self.has_transaction_ = 0;
    if self.transaction_ is not None: self.transaction_.Clear()

  def has_transaction(self): return self.has_transaction_


  def MergeFrom(self, x):
    assert x is not self
    for i in xrange(x.key_size()): self.add_key().CopyFrom(x.key(i))
    if (x.has_transaction()): self.mutable_transaction().MergeFrom(x.transaction())

  def Equals(self, x):
    if x is self: return 1
    if len(self.key_) != len(x.key_): return 0
    for e1, e2 in zip(self.key_, x.key_):
      if e1 != e2: return 0
    if self.has_transaction_ != x.has_transaction_: return 0
    if self.has_transaction_ and self.transaction_ != x.transaction_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    for p in self.key_:
      if not p.IsInitialized(debug_strs): initialized=0
    if (self.has_transaction_ and not self.transaction_.IsInitialized(debug_strs)): initialized = 0
    return initialized

  def ByteSize(self):
    n = 0
    n += 1 * len(self.key_)
    for i in xrange(len(self.key_)): n += self.lengthString(self.key_[i].ByteSize())
    if (self.has_transaction_): n += 1 + self.lengthString(self.transaction_.ByteSize())
    return n + 0

  def Clear(self):
    self.clear_key()
    self.clear_transaction()

  def OutputUnchecked(self, out):
    if (self.has_transaction_):
      out.putVarInt32(42)
      out.putVarInt32(self.transaction_.ByteSize())
      self.transaction_.OutputUnchecked(out)
    for i in xrange(len(self.key_)):
      out.putVarInt32(50)
      out.putVarInt32(self.key_[i].ByteSize())
      self.key_[i].OutputUnchecked(out)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 42:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.mutable_transaction().TryMerge(tmp)
        continue
      if tt == 50:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_key().TryMerge(tmp)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    cnt=0
    for e in self.key_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("key%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    if self.has_transaction_:
      res+=prefix+"transaction <\n"
      res+=self.transaction_.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
    return res

  kkey = 6
  ktransaction = 5

  _TEXT = (
   "ErrorCode",
   None,
   None,
   None,
   None,
   "transaction",
   "key",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.MAX_TYPE,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.STRING,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class NextRequest(ProtocolBuffer.ProtocolMessage):
  has_cursor_ = 0
  has_count_ = 0
  count_ = 1

  def __init__(self, contents=None):
    self.cursor_ = Cursor()
    if contents is not None: self.MergeFromString(contents)

  def cursor(self): return self.cursor_

  def mutable_cursor(self): self.has_cursor_ = 1; return self.cursor_

  def clear_cursor(self):self.has_cursor_ = 0; self.cursor_.Clear()

  def has_cursor(self): return self.has_cursor_

  def count(self): return self.count_

  def set_count(self, x):
    self.has_count_ = 1
    self.count_ = x

  def clear_count(self):
    self.has_count_ = 0
    self.count_ = 1

  def has_count(self): return self.has_count_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_cursor()): self.mutable_cursor().MergeFrom(x.cursor())
    if (x.has_count()): self.set_count(x.count())

  def Equals(self, x):
    if x is self: return 1
    if self.has_cursor_ != x.has_cursor_: return 0
    if self.has_cursor_ and self.cursor_ != x.cursor_: return 0
    if self.has_count_ != x.has_count_: return 0
    if self.has_count_ and self.count_ != x.count_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (not self.has_cursor_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: cursor not set.')
    elif not self.cursor_.IsInitialized(debug_strs): initialized = 0
    return initialized

  def ByteSize(self):
    n = 0
    n += self.lengthString(self.cursor_.ByteSize())
    if (self.has_count_): n += 1 + self.lengthVarInt64(self.count_)
    return n + 1

  def Clear(self):
    self.clear_cursor()
    self.clear_count()

  def OutputUnchecked(self, out):
    out.putVarInt32(10)
    out.putVarInt32(self.cursor_.ByteSize())
    self.cursor_.OutputUnchecked(out)
    if (self.has_count_):
      out.putVarInt32(16)
      out.putVarInt32(self.count_)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.mutable_cursor().TryMerge(tmp)
        continue
      if tt == 16:
        self.set_count(d.getVarInt32())
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_cursor_:
      res+=prefix+"cursor <\n"
      res+=self.cursor_.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
    if self.has_count_: res+=prefix+("count: %s\n" % self.DebugFormatInt32(self.count_))
    return res

  kcursor = 1
  kcount = 2

  _TEXT = (
   "ErrorCode",
   "cursor",
   "count",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.NUMERIC,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class QueryResult(ProtocolBuffer.ProtocolMessage):
  has_cursor_ = 0
  cursor_ = None
  has_more_results_ = 0
  more_results_ = 0

  def __init__(self, contents=None):
    self.result_ = []
    self.lazy_init_lock_ = thread.allocate_lock()
    if contents is not None: self.MergeFromString(contents)

  def cursor(self):
    if self.cursor_ is None:
      self.lazy_init_lock_.acquire()
      try:
        if self.cursor_ is None: self.cursor_ = Cursor()
      finally:
        self.lazy_init_lock_.release()
    return self.cursor_

  def mutable_cursor(self): self.has_cursor_ = 1; return self.cursor()

  def clear_cursor(self):
    self.has_cursor_ = 0;
    if self.cursor_ is not None: self.cursor_.Clear()

  def has_cursor(self): return self.has_cursor_

  def result_size(self): return len(self.result_)
  def result_list(self): return self.result_

  def result(self, i):
    return self.result_[i]

  def mutable_result(self, i):
    return self.result_[i]

  def add_result(self):
    x = EntityProto()
    self.result_.append(x)
    return x

  def clear_result(self):
    self.result_ = []
  def more_results(self): return self.more_results_

  def set_more_results(self, x):
    self.has_more_results_ = 1
    self.more_results_ = x

  def clear_more_results(self):
    self.has_more_results_ = 0
    self.more_results_ = 0

  def has_more_results(self): return self.has_more_results_


  def MergeFrom(self, x):
    assert x is not self
    if (x.has_cursor()): self.mutable_cursor().MergeFrom(x.cursor())
    for i in xrange(x.result_size()): self.add_result().CopyFrom(x.result(i))
    if (x.has_more_results()): self.set_more_results(x.more_results())

  def Equals(self, x):
    if x is self: return 1
    if self.has_cursor_ != x.has_cursor_: return 0
    if self.has_cursor_ and self.cursor_ != x.cursor_: return 0
    if len(self.result_) != len(x.result_): return 0
    for e1, e2 in zip(self.result_, x.result_):
      if e1 != e2: return 0
    if self.has_more_results_ != x.has_more_results_: return 0
    if self.has_more_results_ and self.more_results_ != x.more_results_: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    if (self.has_cursor_ and not self.cursor_.IsInitialized(debug_strs)): initialized = 0
    for p in self.result_:
      if not p.IsInitialized(debug_strs): initialized=0
    if (not self.has_more_results_):
      initialized = 0
      if debug_strs is not None:
        debug_strs.append('Required field: more_results not set.')
    return initialized

  def ByteSize(self):
    n = 0
    if (self.has_cursor_): n += 1 + self.lengthString(self.cursor_.ByteSize())
    n += 1 * len(self.result_)
    for i in xrange(len(self.result_)): n += self.lengthString(self.result_[i].ByteSize())
    return n + 2

  def Clear(self):
    self.clear_cursor()
    self.clear_result()
    self.clear_more_results()

  def OutputUnchecked(self, out):
    if (self.has_cursor_):
      out.putVarInt32(10)
      out.putVarInt32(self.cursor_.ByteSize())
      self.cursor_.OutputUnchecked(out)
    for i in xrange(len(self.result_)):
      out.putVarInt32(18)
      out.putVarInt32(self.result_[i].ByteSize())
      self.result_[i].OutputUnchecked(out)
    out.putVarInt32(24)
    out.putBoolean(self.more_results_)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.mutable_cursor().TryMerge(tmp)
        continue
      if tt == 18:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_result().TryMerge(tmp)
        continue
      if tt == 24:
        self.set_more_results(d.getBoolean())
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    if self.has_cursor_:
      res+=prefix+"cursor <\n"
      res+=self.cursor_.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
    cnt=0
    for e in self.result_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("result%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    if self.has_more_results_: res+=prefix+("more_results: %s\n" % self.DebugFormatBool(self.more_results_))
    return res

  kcursor = 1
  kresult = 2
  kmore_results = 3

  _TEXT = (
   "ErrorCode",
   "cursor",
   "result",
   "more_results",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.STRING,

   ProtocolBuffer.Encoder.NUMERIC,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class Schema(ProtocolBuffer.ProtocolMessage):

  def __init__(self, contents=None):
    self.kind_ = []
    if contents is not None: self.MergeFromString(contents)

  def kind_size(self): return len(self.kind_)
  def kind_list(self): return self.kind_

  def kind(self, i):
    return self.kind_[i]

  def mutable_kind(self, i):
    return self.kind_[i]

  def add_kind(self):
    x = EntityProto()
    self.kind_.append(x)
    return x

  def clear_kind(self):
    self.kind_ = []

  def MergeFrom(self, x):
    assert x is not self
    for i in xrange(x.kind_size()): self.add_kind().CopyFrom(x.kind(i))

  def Equals(self, x):
    if x is self: return 1
    if len(self.kind_) != len(x.kind_): return 0
    for e1, e2 in zip(self.kind_, x.kind_):
      if e1 != e2: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    for p in self.kind_:
      if not p.IsInitialized(debug_strs): initialized=0
    return initialized

  def ByteSize(self):
    n = 0
    n += 1 * len(self.kind_)
    for i in xrange(len(self.kind_)): n += self.lengthString(self.kind_[i].ByteSize())
    return n + 0

  def Clear(self):
    self.clear_kind()

  def OutputUnchecked(self, out):
    for i in xrange(len(self.kind_)):
      out.putVarInt32(10)
      out.putVarInt32(self.kind_[i].ByteSize())
      self.kind_[i].OutputUnchecked(out)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_kind().TryMerge(tmp)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    cnt=0
    for e in self.kind_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("kind%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    return res

  kkind = 1

  _TEXT = (
   "ErrorCode",
   "kind",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STRING,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""
class CompositeIndices(ProtocolBuffer.ProtocolMessage):

  def __init__(self, contents=None):
    self.index_ = []
    if contents is not None: self.MergeFromString(contents)

  def index_size(self): return len(self.index_)
  def index_list(self): return self.index_

  def index(self, i):
    return self.index_[i]

  def mutable_index(self, i):
    return self.index_[i]

  def add_index(self):
    x = CompositeIndex()
    self.index_.append(x)
    return x

  def clear_index(self):
    self.index_ = []

  def MergeFrom(self, x):
    assert x is not self
    for i in xrange(x.index_size()): self.add_index().CopyFrom(x.index(i))

  def Equals(self, x):
    if x is self: return 1
    if len(self.index_) != len(x.index_): return 0
    for e1, e2 in zip(self.index_, x.index_):
      if e1 != e2: return 0
    return 1

  def __eq__(self, other):
    return (other is not None) and (other.__class__ == self.__class__) and self.Equals(other)

  def __ne__(self, other):
    return not (self == other)

  def IsInitialized(self, debug_strs=None):
    initialized = 1
    for p in self.index_:
      if not p.IsInitialized(debug_strs): initialized=0
    return initialized

  def ByteSize(self):
    n = 0
    n += 1 * len(self.index_)
    for i in xrange(len(self.index_)): n += self.lengthString(self.index_[i].ByteSize())
    return n + 0

  def Clear(self):
    self.clear_index()

  def OutputUnchecked(self, out):
    for i in xrange(len(self.index_)):
      out.putVarInt32(10)
      out.putVarInt32(self.index_[i].ByteSize())
      self.index_[i].OutputUnchecked(out)

  def TryMerge(self, d):
    while d.avail() > 0:
      tt = d.getVarInt32()
      if tt == 10:
        length = d.getVarInt32()
        tmp = ProtocolBuffer.Decoder(d.buffer(), d.pos(), d.pos() + length)
        d.skip(length)
        self.add_index().TryMerge(tmp)
        continue
      if (tt == 0): raise ProtocolBuffer.ProtocolBufferDecodeError
      d.skipData(tt)


  def __str__(self, prefix="", printElemNumber=0):
    res=""
    cnt=0
    for e in self.index_:
      elm=""
      if printElemNumber: elm="(%d)" % cnt
      res+=prefix+("index%s <\n" % elm)
      res+=e.__str__(prefix + "  ", printElemNumber)
      res+=prefix+">\n"
      cnt+=1
    return res

  kindex = 1

  _TEXT = (
   "ErrorCode",
   "index",
  )

  _TYPES = (
   ProtocolBuffer.Encoder.NUMERIC,
   ProtocolBuffer.Encoder.STRING,

  )

  _STYLE = """"""
  _STYLE_CONTENT_TYPE = """"""

__all__ = ['Transaction','Query','Query_Filter','Query_Order','QueryExplanation','Cursor','Error','GetRequest','GetResponse','GetResponse_Entity','PutRequest','PutResponse','DeleteRequest','NextRequest','QueryResult','Schema','CompositeIndices']
