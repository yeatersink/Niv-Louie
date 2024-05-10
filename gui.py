from nicegui import app, ui

app.native.window_args["resizable"]=False
app.native.start_args["debug"]=True
ui.label("welcome!")
ui.button("click here")
ui.run(native=True,window_size=(400,300),fullscreen=False,title="example")