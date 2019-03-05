Sub TickerStockVolume():

    ' Variable for holding individual ticker names
    Dim Ticker As String

    ' Variable for holding total stock value per ticker
    Dim Total_Stock_Volume As Double
    Total_Stock_Volume = 0

    ' To populate summary table row by ro
    Dim Table_Row As Integer
    Table_Row = 2

        ' Loop through all rows for 2015
        For i = 2 To 760192

            If Cells(i + 1, 1).Value <> Cells(i, 1).Value Then

            Ticker = Cells(i, 1).Value

            Total_Stock_Value = Total_Stock_Value + Cells(i, 7).Value

            Range("J" & Table_Row).Value = Ticker

            Range("K" & Table_Row).Value = Total_Stock_Value

            Table_Row = Table_Row + 1

            Total_Stock_Value = 0

        Else

            Total_Stock_Volume = Total_Stock_Volume + Cells(i, 7).Value

        End If

    Next i


End Sub
