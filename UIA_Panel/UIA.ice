module UIA
{
    // struct Payload {
    //     string emu1;
    //     string ev1_supply;
    //     string ev1_waste;
    //     string emu1_O2;
    //     string emu2;
    //     string ev2_supply;
    //     string ev2_waste;
    //     string emu2_O2;     
    //     string O2_vent;
    //     string depress_pump;   
    // };

    dictionary<string, string> panelState;

    interface PanelSwitches
    {
        void sendState(dictionary<string, string> panelState);
    }
}