import pymoos
import time

# A simple example using the CMOOSApp wrapper:
# a) we make an app object and set up callbacks for the application lifecycle
# b) we run the app which starts the main loop
# The app class provides a more structured approach than comms, with separate
# callbacks for startup, iteration, and mail handling

app = pymoos.app()

# OnStartUp is called when the app first starts
def on_startup():
    print("App starting up...")
    
    # Read configuration from the mission file
    # The mission file should have a ProcessConfig block for this app
    success, freq = app.get_configuration_double('app_freq')
    if success:
        print(f"Setting app frequency from config: {freq} Hz")
        app.set_app_freq(freq)
    else:
        print("Using default app frequency: 1.0 Hz")
        app.set_app_freq(1.0)
    
    success, comms_freq = app.get_configuration_double('comms_freq')
    if success:
        print(f"Setting comms frequency from config: {comms_freq} Hz")
        app.set_comms_freq(comms_freq)
    else:
        print("Using default comms frequency: 5.0 Hz")
        app.set_comms_freq(5.0)
    
    # Read other configuration parameters
    success, var_name = app.get_configuration_string('variable_name')
    if success:
        print(f"Will publish to variable: {var_name}")
    
    return True

# OnConnectToServer is called when connection to MOOSDB is established
def on_connect_to_server():
    print("Connected to MOOSDB, registering for variables...")
    return app.register('simple_app_var', 0)

# OnNewMail is called when new mail arrives
def on_new_mail(mail):
    print(f"Received {len(mail)} messages:")
    for msg in mail:
        msg.trace()
    return True

# Iterate is the main work loop, called at the frequency set by set_app_freq
iteration_count = 0
def iterate():
    global iteration_count
    iteration_count += 1
    print(f"Iterate #{iteration_count}")
    
    # Publish a message
    app.notify('simple_app_var', f'iteration {iteration_count}', pymoos.time())
    
    # Run for 10 iterations then stop
    if iteration_count >= 10:
        return False
    
    return True

def main():
    # Set up the callbacks
    app.set_on_start_up_callback(on_startup)
    app.set_on_connect_to_server_callback(on_connect_to_server)
    app.set_on_new_mail_callback(on_new_mail)
    app.set_iterate_callback(iterate)
    
    # Run the application (this blocks until iterate returns False)
    # You can optionally provide a mission file path for configuration:
    # app.run('localhost', 9000, 'pymoos_simple_app', 'simpleapp.moos')
    # Or run without a mission file (using defaults in on_startup):
    app.run('localhost', 9000, 'pymoos_simple_app')

if __name__ == "__main__":
    main()
