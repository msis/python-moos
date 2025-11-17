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
    app.set_app_freq(1.0)  # Set how often Iterate is called (Hz)
    app.set_comms_freq(5.0)  # Set how often comms happen (Hz)
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
    app.run('localhost', 9000, 'pymoos_simple_app')

if __name__ == "__main__":
    main()
