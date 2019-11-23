# require 'rinda/rinda'

# URI = "druby://localhost:61676"
# DRb.start_service
# ts = Rinda::TupleSpaceProxy.new(DRbObject.new(nil, URI))
# tuples = [["*", 2, 2 ], [ "+", 2, 5 ], [ "-", 9, 3 ]]
# tuples.each do |t|
#   ts.write(t)
#   res = ts.take(["result", nil])
#   puts "#{res[1]} = #{t[1]} #{t[0]} #{t[2]}"
# end

# clear;python3 arithmetic_client.py
# clear;python arithmetic_client.py

import Arithmetic

ts = Arithmetic.Arithmetic()

tuples = [('*', 2, 2), ('+', 2, 5), ('-', 9, 3)]

for i in tuples:
    r = ts._out(i)
    # print(r)
    res = ts._in(('result', None))
    result = res['output']
    print(f'{result[1]} = {i[1]} {i[0]} {i[2]}')