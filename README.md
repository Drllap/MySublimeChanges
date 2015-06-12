# SublimeMySwitchFile
My Reimplementation of the default sublime command "switch_file"
This implementation sets focus on the requesed file if it is in another 
file group instead of opening it again in the current file group

Add this to sublime-keymap to bind to "alt+o"
{ "keys": ["alt+o"], "command": "my_switch_file", "args": {"extensions": ["cpp", "cxx", "cc", "c", "hpp", "hxx", "hh", "h", "ipp", "inl", "m", "mm"]} }
