import sys
import csv
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

class ChangeMedicationWindow(QtWidgets.QWidget):
    def __init__(self):
        super(ChangeMedicationWindow, self).__init__()
        uic.loadUi("../frontend/medicine.ui", self)  # Load the .ui file

        # Connect buttons to their respective methods
        self.buttonEditMedication.clicked.connect(self.edit_selected_medication)
        self.buttonAddTiming.clicked.connect(self.add_timing)
        self.buttonRemoveTiming.clicked.connect(self.remove_timing)
        self.buttonAddMedication.clicked.connect(self.add_medication)
        self.buttonRemoveMedication.clicked.connect(self.remove_medication)
        self.buttonSaveChanges.clicked.connect(self.save_changes)
        self.editingRow = -1  # Add this line to track the row currently being edited

        # Initialize the medication list table
        self.tableWidgetMedicationList.setRowCount(0)
        self.load_data()  # Load data from CSV on startup

    def load_data(self):
        try:
            with open('medications.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip the header
                for row in reader:
                    self.add_medication_to_table(row[0], row[1], row[2])
        except FileNotFoundError:
            print("The CSV file doesn't exist yet. A new one will be created upon saving.")

    def add_medication_to_table(self, name, timings, slot_number):
        row_position = self.tableWidgetMedicationList.rowCount()
        self.tableWidgetMedicationList.insertRow(row_position)
        self.tableWidgetMedicationList.setItem(row_position, 0, QtWidgets.QTableWidgetItem(name))
        self.tableWidgetMedicationList.setItem(row_position, 1, QtWidgets.QTableWidgetItem(timings))
        self.tableWidgetMedicationList.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(slot_number)))

    def save_changes(self):
        with open('medications.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Medication Name', 'Timings', 'Slot Number'])
            for row in range(self.tableWidgetMedicationList.rowCount()):
                name = self.tableWidgetMedicationList.item(row, 0).text()
                timings = self.tableWidgetMedicationList.item(row, 1).text()
                slot_number = self.tableWidgetMedicationList.item(row, 2).text()
                writer.writerow([name, timings, slot_number])
        print("Changes saved to the CSV file")

    def add_timing(self):
        new_timing = self.lineEditNewTiming.text().strip()
        if new_timing:
            self.listWidgetMedicationTimings.addItem(new_timing)
            self.lineEditNewTiming.clear()
        else:
            print("No timing entered")

    def remove_timing(self):
        selected_item = self.listWidgetMedicationTimings.currentItem()
        if selected_item:
            self.listWidgetMedicationTimings.takeItem(self.listWidgetMedicationTimings.row(selected_item))
        else:
            print("No timing selected")

    def add_medication(self):
        medication_name = self.lineEditMedicationName.text()
        slot_number = self.spinBoxSlotNumber.value()
        timings = [self.listWidgetMedicationTimings.item(i).text() for i in range(self.listWidgetMedicationTimings.count())]

        if medication_name and timings:
            if self.editingRow >= 0:  # Check if we're editing
                # Validate slot number before updating
                if self.validate_slot_number(slot_number, self.editingRow):
                    self.update_medication_in_table(self.editingRow, medication_name, ", ".join(timings), str(slot_number))
                    self.editingRow = -1  # Reset editing state
                    self.save_changes()
                else:
                    QMessageBox.warning(self, "Slot Unavailable", f"Slot {slot_number} is already in use. Please choose a different slot.")
            else:
                # Validate slot number before adding new medication
                if self.validate_slot_number(slot_number):
                    self.add_medication_to_table(medication_name, ", ".join(timings), str(slot_number))
                    self.save_changes()
                else:
                    print(f"Slot {slot_number} is already in use. Please choose a different slot.")
        else:
            QMessageBox.warning(self, "Missing Information", "Medication name or timings are missing.")


    def remove_medication(self):
        selected_row = self.tableWidgetMedicationList.currentRow()
        if selected_row >= 0:
            self.tableWidgetMedicationList.removeRow(selected_row)
            # Save changes after removing
            self.save_changes()
        else:
            print("No medication selected to remove")

    def edit_selected_medication(self):
        selected_row = self.tableWidgetMedicationList.currentRow()
        if selected_row >= 0:
            # Load the details into the input fields
            self.lineEditMedicationName.setText(self.tableWidgetMedicationList.item(selected_row, 0).text())
            self.spinBoxSlotNumber.setValue(int(self.tableWidgetMedicationList.item(selected_row, 2).text()))
            timings = self.tableWidgetMedicationList.item(selected_row, 1).text().split(", ")
            self.listWidgetMedicationTimings.clear()
            for timing in timings:
                self.listWidgetMedicationTimings.addItem(timing)
            
            self.editingRow = selected_row  # Track the row being edited


    def update_medication_in_table(self, row, name, timings, slot_number):
        """Updates the medication details in the specified row."""
        self.tableWidgetMedicationList.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
        self.tableWidgetMedicationList.setItem(row, 1, QtWidgets.QTableWidgetItem(timings))
        self.tableWidgetMedicationList.setItem(row, 2, QtWidgets.QTableWidgetItem(str(slot_number)))


    def validate_slot_number(self, slot_number, ignore_row=-1):
        """Checks if the slot number is already in use, ignoring the row specified."""
        for row in range(self.tableWidgetMedicationList.rowCount()):
            if row == ignore_row:
                continue
            if self.tableWidgetMedicationList.item(row, 2) and int(self.tableWidgetMedicationList.item(row, 2).text()) == slot_number:
                return False  # Slot is already in use
        return True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ChangeMedicationWindow()
    window.show()
    sys.exit(app.exec_())
