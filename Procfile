# clear; foreman start
# See <https://www.ruby-forum.com/t/forcing-stdout-sync-for-scripts/48876/8>
alice_ts: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' tuplespace.rb -c alice.yaml
alice_adapter: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' adapter.rb -c alice.yaml
alice_arithmetic_server: python arithmetic_server.py -c alice.yaml

bob_ts: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' tuplespace.rb -c bob.yaml
bob_adapter: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' adapter.rb -c bob.yaml
bob_arithmetic_server: python arithmetic_server.py -c bob.yaml

# chuck_ts: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' tuplespace.rb -c chuck.yaml
# chuck_adapter: ruby -e '$stdout.sync = true; load($0 = ARGV.shift)' adapter.rb -c chuck.yaml
# chuck_arithmetic_server: python arithmetic_server.py -c chuck.yaml

subscribe: python subscribe.py 224.0.0.1 54321

# recovery: python recovery.py 224.0.0.1 54322