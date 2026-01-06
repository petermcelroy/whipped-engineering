' This code belongs to the UserForm "frmUValues".
Private uValueData As Object

Private Sub UserForm_Initialize()
    ' Set up the data structure using a Dictionary object.
    ' Requires a reference to 'Microsoft Scripting Runtime'.
    Set uValueData = CreateObject("Scripting.Dictionary")

    ' --- ENGLAND AND WALES DATA ---
    Dim dataEW As Object
    Set dataEW = CreateObject("Scripting.Dictionary")
    
    Dim dataEW_Domestic As Object
    Set dataEW_Domestic = CreateObject("Scripting.Dictionary")
    dataEW_Domestic.Add "1965", VBA.Array("Walls (Cavity)", "1.7", "Roofs (Pitched)", "1.4", "Floors", "1.4", "Windows (Single Glazing)", "5.7")
    dataEW_Domestic.Add "1976", VBA.Array("Walls (Cavity)", "1.0", "Roofs (Pitched)", "0.6", "Floors", "1.2", "Windows (Single Glazing)", "5.7")
    dataEW_Domestic.Add "1985", VBA.Array("Walls (Cavity)", "0.6", "Roofs (Pitched)", "0.35", "Floors", "0.51", "Windows (Double Glazing)", "4.8")
    dataEW_Domestic.Add "1995", VBA.Array("Walls (Cavity)", "0.45", "Roofs (Pitched)", "0.25", "Floors", "0.25", "Windows (Double Glazing)", "3.3")
    dataEW_Domestic.Add "2002", VBA.Array("Walls (Cavity)", "0.35", "Roofs (Pitched)", "0.16", "Floors", "0.25", "Windows (Double Glazing)", "2.2")
    dataEW_Domestic.Add "2006", VBA.Array("Walls (Cavity)", "0.30", "Roofs (Pitched)", "0.20", "Floors", "0.22", "Windows (Double Glazing)", "2.0")
    dataEW_Domestic.Add "2010", VBA.Array("Walls (Cavity)", "0.28", "Roofs (Pitched)", "0.18", "Floors", "0.22", "Windows (Double Glazing)", "1.8")
    dataEW_Domestic.Add "2013", VBA.Array("Walls (Cavity)", "0.18", "Roofs (Pitched)", "0.13", "Floors", "0.13", "Windows (Double Glazing)", "1.4")
    dataEW_Domestic.Add "2022", VBA.Array("Walls (Cavity)", "0.18", "Roofs (Pitched)", "0.11", "Floors", "0.13", "Windows (Double Glazing)", "1.2")
    dataEW.Add "Domestic", dataEW_Domestic
    
    Dim dataEW_NonDomestic As Object
    Set dataEW_NonDomestic = CreateObject("Scripting.Dictionary")
    dataEW_NonDomestic.Add "1965", VBA.Array("Walls", "1.7", "Roofs", "1.4", "Floors", "1.4", "Windows", "5.7")
    dataEW_NonDomestic.Add "1976", VBA.Array("Walls", "1.0", "Roofs", "0.6", "Floors", "1.2", "Windows", "5.7")
    dataEW_NonDomestic.Add "1985", VBA.Array("Walls", "0.6", "Roofs", "0.35", "Floors", "0.51", "Windows", "4.8")
    dataEW_NonDomestic.Add "1995", VBA.Array("Walls", "0.45", "Roofs", "0.25", "Floors", "0.25", "Windows", "3.3")
    dataEW_NonDomestic.Add "2002", VBA.Array("Walls", "0.35", "Roofs", "0.16", "Floors", "0.25", "Windows", "2.2")
    dataEW_NonDomestic.Add "2006", VBA.Array("Walls", "0.30", "Roofs", "0.20", "Floors", "0.22", "Windows", "2.0")
    dataEW_NonDomestic.Add "2010", VBA.Array("Walls", "0.28", "Roofs", "0.18", "Floors", "0.22", "Windows", "1.8")
    dataEW_NonDomestic.Add "2013", VBA.Array("Walls", "0.18", "Roofs", "0.13", "Floors", "0.13", "Windows", "1.4")
    dataEW_NonDomestic.Add "2022", VBA.Array("Walls", "0.18", "Roofs", "0.11", "Floors", "0.13", "Windows", "1.2")
    dataEW.Add "Non-Domestic", dataEW_NonDomestic
    
    uValueData.Add "England and Wales", dataEW

    ' --- SCOTLAND DATA ---
    Dim dataSC As Object
    Set dataSC = CreateObject("Scripting.Dictionary")

    Dim dataSC_Domestic As Object
    Set dataSC_Domestic = CreateObject("Scripting.Dictionary")
    dataSC_Domestic.Add "1963", VBA.Array("Walls", "1.7", "Roofs", "1.4", "Floors", "1.4", "Windows", "5.7")
    dataSC_Domestic.Add "1985", VBA.Array("Walls", "0.6", "Roofs", "0.35", "Floors", "0.51", "Windows", "4.8")
    dataSC_Domestic.Add "1999", VBA.Array("Walls", "0.45", "Roofs", "0.25", "Floors", "0.22", "Windows", "3.1")
    dataSC_Domestic.Add "2002", VBA.Array("Walls", "0.30", "Roofs", "0.20", "Floors", "0.22", "Windows", "2.0")
    dataSC_Domestic.Add "2007", VBA.Array("Walls", "0.27", "Roofs", "0.16", "Floors", "0.18", "Windows", "1.6")
    dataSC_Domestic.Add "2010", VBA.Array("Walls", "0.22", "Roofs", "0.15", "Floors", "0.15", "Windows", "1.6")
    dataSC_Domestic.Add "2015", VBA.Array("Walls", "0.17", "Roofs", "0.11", "Floors", "0.12", "Windows", "1.4")
    dataSC_Domestic.Add "2022", VBA.Array("Walls", "0.17", "Roofs", "0.12", "Floors", "0.15", "Windows", "1.4")
    dataSC.Add "Domestic", dataSC_Domestic

    Dim dataSC_NonDomestic As Object
    Set dataSC_NonDomestic = CreateObject("Scripting.Dictionary")
    dataSC_NonDomestic.Add "1963", VBA.Array("Walls", "1.7", "Roofs", "1.4", "Floors", "1.4", "Windows", "5.7")
    dataSC_NonDomestic.Add "1985", VBA.Array("Walls", "0.6", "Roofs", "0.35", "Floors", "0.51", "Windows", "4.8")
    dataSC_NonDomestic.Add "1999", VBA.Array("Walls", "0.45", "Roofs", "0.25", "Floors", "0.22", "Windows", "3.1")
    dataSC_NonDomestic.Add "2002", VBA.Array("Walls", "0.30", "Roofs", "0.20", "Floors", "0.22", "Windows", "2.0")
    dataSC_NonDomestic.Add "2007", VBA.Array("Walls", "0.27", "Roofs", "0.16", "Floors", "0.18", "Windows", "1.6")
    dataSC_NonDomestic.Add "2010", VBA.Array("Walls", "0.22", "Roofs", "0.15", "Floors", "0.15", "Windows", "1.6")
    dataSC_NonDomestic.Add "2015", VBA.Array("Walls", "0.17", "Roofs", "0.11", "Floors", "0.12", "Windows", "1.4")
    dataSC_NonDomestic.Add "2022", VBA.Array("Walls", "0.17", "Roofs", "0.12", "Floors", "0.15", "Windows", "1.4")
    dataSC.Add "Non-Domestic", dataSC_NonDomestic

    uValueData.Add "Scotland", dataSC

    ' Populate the country combo box
    Dim key As Variant
    For Each key In uValueData.Keys
        Me.cboCountry.AddItem key
    Next key
End Sub

Private Sub cboCountry_Change()
    ' Clear and reset the other combo boxes
    Me.cboBuildingType.Clear
    Me.cboYear.Clear
    
    If Me.cboCountry.ListIndex >= 0 Then
        Dim selectedCountry As String
        selectedCountry = Me.cboCountry.Text
        
        Dim buildingTypes As Object
        Set buildingTypes = uValueData(selectedCountry)
        
        Dim key As Variant
        For Each key In buildingTypes.Keys
            Me.cboBuildingType.AddItem key
        Next key
    End If
End Sub

Private Sub cboBuildingType_Change()
    ' Clear and reset the year combo box
    Me.cboYear.Clear
    
    If Me.cboBuildingType.ListIndex >= 0 Then
        Dim selectedCountry As String
        selectedCountry = Me.cboCountry.Text
        
        Dim selectedBuildingType As String
        selectedBuildingType = Me.cboBuildingType.Text
        
        Dim yearsData As Object
        Set yearsData = uValueData(selectedCountry)(selectedBuildingType)
        
        Dim key As Variant
        For Each key In yearsData.Keys
            Me.cboYear.AddItem key
        Next key
    End If
End Sub

Private Sub cmdGenerate_Click()
    ' Validate that all selections have been made
    If Me.cboCountry.ListIndex = -1 Or Me.cboBuildingType.ListIndex = -1 Or Me.cboYear.ListIndex = -1 Then
        MsgBox "Please select a country, building type, and year.", vbExclamation, "Missing Information"
        Exit Sub
    End If
    
    Dim selectedCountry As String
    selectedCountry = Me.cboCountry.Text
    
    Dim selectedBuildingType As String
    selectedBuildingType = Me.cboBuildingType.Text
    
    Dim selectedYear As String
    selectedYear = Me.cboYear.Text
    
    ' Get the data array for the selection
    Dim dataArray As Variant
    dataArray = uValueData(selectedCountry)(selectedBuildingType)(selectedYear)
    
    ' Generate the table in the Word document
    Call GenerateUValueTable(selectedCountry, selectedBuildingType, selectedYear, dataArray)
    
    ' Hide the form after generating the table
    Me.Hide
End Sub
