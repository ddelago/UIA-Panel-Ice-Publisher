module UIA
{

    dictionary<string, string> panelState;

    interface PanelSwitches
    {
        void sendState(panelState p);
    }
}