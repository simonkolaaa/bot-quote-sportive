import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class Reporter:
    def __init__(self):
        self.telegram_token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")

    def generate_excel(self, data_list, filename="Top_Giocate_Weekend.xlsx"):
        if not data_list:
            print("⚠️ Nessun dato da inserire nell'Excel.")
            return None
            
        df = pd.DataFrame(data_list)
        
        # Riordina le colonne se presenti
        standard_order = [
            "Campionato", "Squadra_Casa", "Squadra_Trasferta", 
            "Quota_Eurobet", "Affidabilita_1_10", 
            "Giocata_Suggerita", "Consiglio_Pengwin", "Analisi_Tecnica"
        ]
        
        # Filtra solo le colonne effettivamente presenti nei dati
        existing_cols = [c for c in standard_order if c in df.columns]
        other_cols = [c for c in df.columns if c not in standard_order]
        df = df[existing_cols + other_cols]

        try:
            from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Pronostici')
                worksheet = writer.sheets['Pronostici']
                
                # Stili Header
                header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
                header_font = Font(color="FFFFFF", bold=True, size=12)
                center_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                left_wrap_alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

                # Applica stile alle intestazioni
                for cell in worksheet[1]:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = center_alignment
                    cell.border = thin_border
                    
                # Formattazione Colonne e Celle Dati
                for col_idx, col in enumerate(df.columns, 1):
                    col_letter = worksheet.cell(row=1, column=col_idx).column_letter
                    
                    # Imposta larghezza in base al tipo di colonna
                    if col in ["Analisi_Tecnica", "Consiglio_Pengwin"]:
                        worksheet.column_dimensions[col_letter].width = 60
                        align = left_wrap_alignment
                    elif col in ["Squadra_Casa", "Squadra_Trasferta", "Match"]:
                        worksheet.column_dimensions[col_letter].width = 20
                        align = center_alignment
                    elif col == "Giocata_Suggerita":
                        worksheet.column_dimensions[col_letter].width = 25
                        align = center_alignment
                        # Grassetto per la giocata suggerita
                    else:
                        worksheet.column_dimensions[col_letter].width = 16
                        align = center_alignment
                        
                    # Applica allineamento e bordi alle righe dati
                    for row in range(2, len(df) + 2):
                        cell = worksheet.cell(row=row, column=col_idx)
                        cell.alignment = align
                        cell.border = thin_border
                        if col == "Giocata_Suggerita":
                            cell.font = Font(bold=True, color="000000")
                            cell.fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid") # Sfondo verdino leggero

            print(f"✅ Report Excel formattato generato con successo: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Errore nella generazione Excel: {e}")
            return None

    def send_to_telegram(self, file_path, caption="📊 Analisi premium del weekend pronta!"):
        if not self.telegram_token or not self.chat_id:
            print("Telegram Token o Chat ID non configurati")
            return False

        url = f"https://api.telegram.org/bot{self.telegram_token}/sendDocument"
        
        try:
            with open(file_path, "rb") as file:
                files = {"document": file}
                data = {"chat_id": self.chat_id, "caption": caption}
                response = requests.post(url, files=files, data=data)
                
                if response.status_code == 200:
                    print("File inviato correttamente su Telegram.")
                    return True
                else:
                    print(f"Errore invio Telegram: {response.text}")
                    return False
        except Exception as e:
            print(f"Errore durante l'invio Telegram: {e}")
            return False

if __name__ == "__main__":
    # Test
    # reporter = Reporter()
    # reporter.generate_excel([{"Test": "Successo"}])
    pass
