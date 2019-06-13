//=======================================================================================
// File: eproc_slice.ice
// Creator: Larry Garner - ER6
// Date: Apr 14, 2015
// Version: 0.0.1

// Change History

//=======================================================================================


module gov {
	module nasa {
		module jsc {
			module er {
					
					// Constants defining the names of the ICE topics 
					const string cmdTopicName		= "eproc_cmd_topic";
					const string tlmTopicName		= "eproc_tlm_topic";

					// defines the existence of string array
					sequence<string>	seqString;
					
					/**********************************************************************
					 *	COMMON MESSAGE HEADER
					 *	Notes:
					 *		srcName & messageName will be used to lookup the message id for a Telemetry Message
					 *		destName will be used to lookup the message id for a Command Message
					 **********************************************************************/
					struct MessageHeader {
						double	time;			// current time in <secs.millisecs> format
						
						string messageName;		// name of the message (example: TLM_OUT_DATA, COMMAND)
												// this is required for telemetry messages
												// this is not required for command messages since all commands messages are mapped to the same message id
												
						string	srcName;		// name of the software interface that publishes the message
												// this is required for telemetry messages
												// this is not required for command messages
												
						string 	destName;		// name of the software interface that receives(the intended target) the message
												// this is required for command messages
												// this is not required for telemetry messages
					};


					/**********************************************************************
					 *	COMMAND STRUCTS & INTERFACE
					 *	Notes:
					 *		cmdId is equivalent to a command code
					 *		
					 **********************************************************************/
					struct CommandData {
						short		cmdId;	// same as command code in CCSDS
						seqString	args;	// each arg regardless of data type is stored as a string
											// so the arguments could be
											// args[0] = "3.14"
											// args[1] = "54"
											// args[2] = "stop"
					};
					// command message struct
					struct CommandMessage {
						MessageHeader   hdr;
						CommandData  data;
					};
					
					interface Command {
						void transfer(CommandMessage message);
					};

					

					/*************************************************************************************
					 *  TELEMETRY STRUCTS & INTERFACE
					 *************************************************************************************/
					// represents a single telemetry item
					struct TelemetryData {
						string		id;		// this will hold a PUI, CUI, MSID, or other unique identifier
						string		value;	// this will hold the telemetry's value
					};
					// define a collection of TelemetryData
					sequence<TelemetryData>	seqTelemetryData;
					
					// represents a telemetry message
					// the message can contain any number of telemetry items
					struct TelemetryMessage {
						MessageHeader		hdr;
						seqTelemetryData	data;
					};
					
					
					interface Telemetry {
						void transfer(TelemetryMessage message);
					};

			};
		};
	};
};
