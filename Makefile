install:
	install -m700 ./set_space_switch.py /usr/local/bin/
	install -m700 ./set_space_display_switch.py /usr/local/bin/

uninstall:
	rm /usr/local/bin/set_space_switch.py
	rm /usr/local/bin/set_space_display_switch.py