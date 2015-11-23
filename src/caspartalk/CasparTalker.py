import json
import ResponseInterpreter


class CasparTalker:
    # CasparTalker is kind of a translation layer between the interface and Casper's
    # control protocol (currently AMCP).
    # It will build the correct AMCP string for a given command, tell the
    # CasparServer to send it, and handles the response.

    def __init__(self):
        pass

    def send_command_to_caspar(self, server, amcp_command):
        print "Sending command:", amcp_command
        if not amcp_command.endswith("\r\n"): amcp_command += "\r\n"
        server.send_command(amcp_command)

        response = server.read_until("\r\n")

        # ResponseInterpreter lets us know how to proceed - Caspar's way of sending information
        # is a bit vague.
        to_do = ResponseInterpreter.interpret_response(response)
        if to_do[1]:
            return server.read_until(to_do[2])
        else:
            return None

    # Data commands - create and manipulate datasets

    def data_store(self, server, name, data):
        # DATA STORE [name:string] [data:string]
        # Stores the dataset data under the name name.
        # Directories will be created if they do not exist.

        data = json.dumps(data)  # Escape quotes, etc.
        amcp_string = "DATA STORE {name} {data}".format(name=name, data=data)

        self.send_command_to_caspar(server, amcp_string)

    def data_retrieve(self, server, name):
        # DATA RETRIEVE [name:string]
        # Returns the data saved under the name name.

        amcp_string = "DATA RETRIEVE {name}".format(name=name)

        data = self.send_command_to_caspar(server, amcp_string)
        print data

    def data_list(self, server):
        # DATA LIST
        # Returns a list of all stored datasets.

        amcp_string = "DATA LIST"
        data = self.send_command_to_caspar(server, amcp_string)

    def data_remove(self, server, name):
        # DATA REMOVE [name:string]
        # Removes the dataset saved under the name name.

        amcp_string = "DATA REMOVE {name}".format(name=name)
        self.send_command_to_caspar(server, amcp_string)

    # CG Commands - manipulate Flash templates in Caspar
    def cg_add(self, server, template, channel=1, layer=10, cg_layer=0, play_on_load=0, data=None):
        # CG [video_channel:int]{-[layer:int]|-9999} ADD [cg_layer:int] [template:string] [play-on-load:0,1] {[data]}
        # Prepares a template for displaying.
        # It won't show until you call CG PLAY (unless you supply the play-on-load flag, 1 for true).
        # Data is either inline XML or a reference to a saved dataset.

        data = json.dumps(data)  # Escape quotes, etc.
        amcp_string = "CG {video_channel}-{layer} ADD {cg_layer} {template} {play_on_load} {data}".format(
            video_channel=channel, layer=layer, cg_layer=cg_layer, template=template, play_on_load=play_on_load,
            data=data)

        self.send_command_to_caspar(server, amcp_string)

    def cg_play(self, server, channel=1, layer=10, cg_layer=0):
        # CG [video_channel:int]{-[layer:int]|-9999} PLAY [cg_layer:int]
        # Plays and displays the template in the specified layer.

        amcp_string = "CG {video_channel}-{layer} PLAY {cg_layer}".format(video_channel=channel,
                                                                          layer=layer, cg_layer=cg_layer)

        self.send_command_to_caspar(server, amcp_string)

    def cg_stop(self, server, channel=1, layer=10, cg_layer=0):
        # CG [video_channel:int]{-[layer:int]|-9999} STOP [cg_layer:int]
        # Stops and removes the template from the specified layer.
        # This is different from REMOVE in that the template gets a chance to
        # animate out when it is stopped.

        amcp_string = "CG {video_channel}-{layer} STOP [cg_layer]".format(video_channel=channel, layer=layer,
                                                                          cg_layer=cg_layer)

        self.send_command_to_caspar(server, amcp_string)

    def cg_next(self, server, channel=1, layer=10, cg_layer=0):
        # CG [video_channel:int]{-[layer:int]|-9999} NEXT [cg_layer:int]
        # Triggers a "continue" in the template on the specified layer.
        # This is used to control animations that has multiple discreet steps.

        amcp_string = "CG {video_channel}-{layer} NEXT {cg_layer}".format(video_channel=channel, layer=layer,
                                                                          cg_layer=cg_layer)

        self.send_command_to_caspar(server, amcp_string)

    def cg_remove(self, server, channel=1, layer=10, cg_layer=0):
        # CG [video_channel:int]{-[layer:int]|-9999} REMOVE [cg_layer:int]
        # Removes the template from the specified layer.

        amcp_string = "CG {video_channel}-{layer} REMOVE {cg_layer}".format(video_channel=channel, layer=layer,
                                                                            cg_layer=cg_layer)

        self.send_command_to_caspar(server, amcp_string)

    def cg_clear(self, server, channel=1, layer=10):
        # CG [video_channel:int]{-[layer:int]|-9999} CLEAR
        # Removes all templates on a video layer. The entire cg producer will be removed.

        amcp_string = "CG {video_channel}-{layer} CLEAR".format(video_channel=channel, layer=layer)

        self.send_command_to_caspar(server, amcp_string)

    def cg_update(self, server, channel=1, layer=10, data=None):
        # CG [video_channel:int]{-[layer:int]|-9999} UPDATE [cg_layer:int] [data:string]
        # Sends new data to the template on specified layer.
        # Data is either inline XML or a reference to a saved dataset.

        data = json.dumps(data)  # Escape quotes, etc.
        amcp_string = "CG {video_channel}-{layer} UPDATE {cg_layer} {data}".format(video_channel=channel,
                                                                                   layer=layer, data=data)

        self.send_command_to_caspar(server, amcp_string)

    def cg_invoke(self, server, method, channel=1, layer=0, cg_layer=1):
        # CG [video_channel:int]{-[layer:int]|-9999} INVOKE [cg_layer:int] [method:string]
        # Invokes the given method on the template on the specified layer.
        # Can be used to jump the playhead to a specific label.

        amcp_string = "CG {video_channel}-{layer} INVOKE {cg_layer} {method}".format(video_channel=channel, layer=layer,
                                                                                     cg_layer=cg_layer, method=method)

        self.send_command_to_caspar(server, amcp_string)

    def cg_info(self, server, channel=1, layer=10, cg_layer=1):
        # CG [video_channel:int]{-[layer:int]|-9999} INFO {[cg_layer:int]}
        # Retrieves information about the template on the specified layer.
        # If cg_layer is not given, information about the template host is given instead.

        amcp_string = "CG {video_channel}-{layer} INFO {cg_layer}".format(video_channel=channel, layer=layer,
                                                                          cg_layer=cg_layer)

        print self.send_command_to_caspar(server, amcp_string)
