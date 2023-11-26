import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# Clipboard Manager Class
class ClipboardManager(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hyprboardn")

        # Set window properties
        self.set_default_size(640, 480)
        self.set_resizable(False)
        
        # Set background color
        rgba = Gdk.RGBA()
        rgba.parse("#101010")
        self.override_background_color(Gtk.StateType.NORMAL, rgba)

        # Clipboard Text
        self.clipboard_text = ""

        # Clipboard Entry
        self.clipboard_entry = Gtk.Entry()
        self.clipboard_entry.set_text(self.clipboard_text)
        self.clipboard_entry.set_can_focus(False)

        # Clipboard History ListStore
        self.clipboard_history_store = Gtk.ListStore(str)
        self.clipboard_history_view = Gtk.TreeView(model=self.clipboard_history_store)
        self.clipboard_history_view.set_headers_visible(False)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("History", renderer, text=0)
        self.clipboard_history_view.append_column(column)

        # Clipboard History ScrolledWindow
        clipboard_history_sw = Gtk.ScrolledWindow()
        clipboard_history_sw.set_vexpand(True)
        clipboard_history_sw.set_hexpand(True)
        clipboard_history_sw.add(self.clipboard_history_view)

        # Clear Button
        clear_button = Gtk.Button(label="Clear History")
        clear_button.connect("clicked", self.clear_history)
        
        # Set button color
        rgba_button = Gdk.RGBA()
        rgba_button.parse("#141414")
        clear_button.override_background_color(Gtk.StateType.NORMAL, rgba_button)

        # Main Vertical Box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Add Clipboard Entry, History, and Clear Button to VBox
        vbox.pack_start(self.clipboard_entry, False, False, 0)
        vbox.pack_start(clipboard_history_sw, True, True, 0)
        vbox.pack_start(clear_button, False, False, 0)

        # Connect Clipboard Changed Signal
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.connect("owner-change", self.on_clipboard_changed)

    def on_clipboard_changed(self, clipboard, event):
        # Get clipboard text
        self.clipboard_text = clipboard.wait_for_text()

        # Check if clipboard text is already in the history store
        for row in self.clipboard_history_store:
            if row[0] == self.clipboard_text:
                self.clipboard_history_store.remove(row.iter)
                break

        # Add clipboard text to history store
        self.clipboard_history_store.prepend([self.clipboard_text])

    def clear_history(self, button):
        # Clear the clipboard history
        self.clipboard_history_store.clear()

        # Clear text
        self.clipboard_text = ""

        # Clear entry text
        self.clipboard_entry.set_text("")

    def run(self):
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()

# Run the Clipboard Manager
if __name__ == "__main__":
    clipboard_manager = ClipboardManager()
    clipboard_manager.run()
