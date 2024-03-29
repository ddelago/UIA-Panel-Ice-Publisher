## Adding the Procedure Into eProc
You need to make sure that you have the procedure as well as all of its assets loaded into eProc in order for the procedure to show up and load correctly.
1. Copy `hal-test-pi.prl` to `~\eProcServer\apache-tomee-plume-1.7.4\work\test\procedures\projects\prl\prog\procedures\`
2. Copy `hal-uia.dat`, `hal-uia.xml`, `uia`, and `uia.manifest` to `~\eProcServer\apache-tomee-plume-1.7.4\webapps\ptv\content\`
3. Copy `HAL_3_4.map` to `~\eProcServer\apache-tomee-plume-1.7.4\work\test\procedures\projects\prl\prog\sysrep\`

## Loading CDD File
You need to include the UIA_CDD.XML in order for the procedure to recognize the UIA panel variables.
1. Go to the advanced tab of ePat and select **manage** in the upper right-hand corner
  ![alt text](https://github.com/ddelago/UIA-Panel-Ice-Publisher/blob/master/documentation/ePat1.png)
2. Select Choose File and import the UIA_CDD.XML file
  ![alt text](https://github.com/ddelago/UIA-Panel-Ice-Publisher/blob/master/documentation/ePat2.png)
3. Select UIA_CDD.XML in the table and then publish
  ![alt text](https://github.com/ddelago/UIA-Panel-Ice-Publisher/blob/master/documentation/ePat3.png)
