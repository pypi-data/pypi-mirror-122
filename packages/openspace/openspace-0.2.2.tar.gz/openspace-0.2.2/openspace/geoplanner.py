from openspace.math.time_conversions import epoch_string_to_timestamp
import os
import sys
from PyQt5 import QtWidgets, uic, QtGui
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import random
import pkg_resources
import time

from openspace.catalogs import TwoLineElsets
from openspace.propagators import ClohessyWiltshireModel, TwoBodyModel
from openspace.math.coordinates import (
    cartesian_to_spherical, 
    j2000_to_hill,
    vector_to_coes
    )
from openspace.math.measurements import Distance, Angle, Epoch
from openspace.math.time_conversions import (
    get_eci_to_ecef_gst_angle,
    SECONDS_IN_MINUTE,
    SECONDS_IN_DAY
    )

class GeoWindow(QtWidgets.QMainWindow):
    def __init__(self):

        super(GeoWindow, self).__init__()
        ui = pkg_resources.resource_filename(
            __name__, 
            "resources/ui_files/geoplanner.ui"
            )
        uic.loadUi(ui, self)

        self.add_object_button.released.connect(self.plot_state)
        self.ca_button.released.connect(self.get_conjunctions)
        self.remove_object_button.released.connect(self.remove_state)
        self.load_active_geo_action.triggered.connect(self.load_active_geo)
        self.download_active_geo.triggered.connect(
            TwoLineElsets.get_latest_celetrak_active_geo
            )

        self.tles = {}
        self.active_sccs = {}
        self.rel_geo_plot.addLegend()

    def remove_state(self):
        row = self.available_sccs_table.currentRow()
        scc = self.available_sccs_table.item(row, 0).text()

        if self.active_sccs.get(scc) is not None:
            self.rel_geo_plot.removeItem(self.active_sccs[scc])
            del self.active_sccs[scc]
            color = QtGui.QColor(255, 255, 255)
            self.available_sccs_table.item(row, 0).setBackground(color)
            self.available_sccs_table.item(row, 1).setBackground(color)

            

    def get_conjunctions(self):

        while self.ca_table.rowCount() > 0:
            self.ca_table.removeRow(0)

        sccs = sorted(self.tles.keys())
        i = 1
        for scc1 in sccs[0:-1]:
            _, r1, v1, name1  = self.tles[scc1]
            a, _, inc, _, aop, raan = vector_to_coes(r1, v1)
            r1 = j2000_to_hill(raan, aop, inc, r1)
            v1 = j2000_to_hill(raan, aop, inc, v1)
            
            for scc2 in sccs[i:]:
                _, r2, v2, name2  = self.tles[scc2]
                r2 = j2000_to_hill(raan, aop, inc, r2)
                v2 = j2000_to_hill(raan, aop, inc, v2)
                rel_pos = r1.minus(r2)
                rel_vel = v1.minus(v2)
                rel_state = [
                    rel_pos.get_element(0),
                    rel_pos.get_element(1),
                    rel_pos.get_element(2),
                    rel_vel.get_element(0),
                    rel_vel.get_element(1),
                    rel_vel.get_element(2)
                ]
                rel_mod = ClohessyWiltshireModel(rel_state, a)

                t, min_range = rel_mod.get_close_approach_over_interval(0, 300, 300)

                if min_range < 200000:
                    row = self.ca_table.rowCount()
                    self.ca_table.insertRow(row)
                    scc_text = QtWidgets.QTableWidgetItem(scc1)
                    name_text = QtWidgets.QTableWidgetItem(name1)
                    self.ca_table.setItem(row , 0, scc_text)
                    self.ca_table.setItem(row , 1, name_text)
                    scc_text = QtWidgets.QTableWidgetItem(scc2)
                    name_text = QtWidgets.QTableWidgetItem(name2)
                    self.ca_table.setItem(row , 2, scc_text)
                    self.ca_table.setItem(row , 3, name_text)
                    range_text = QtWidgets.QTableWidgetItem(str(min_range/1000))
                    self.ca_table.setItem(row , 4, range_text)
                    self.ca_table.resizeColumnToContents(0)
                    self.ca_table.resizeColumnToContents(1)
                    self.ca_table.resizeColumnToContents(2)
                    self.ca_table.resizeColumnToContents(3)
                    self.ca_table.resizeColumnToContents(4)
            i+=1


    def plot_state(self):

        row = self.available_sccs_table.currentRow()
        scc = self.available_sccs_table.item(row, 0).text()

        if self.tles.get(scc) is not None:
            epoch, r0, v0, name  = self.tles[scc]
            get_plot_data = True
        else:
            get_plot_data = False
        
        if get_plot_data and self.active_sccs.get(scc) is None:
            tbm = TwoBodyModel(r0, v0, epoch)
            period = tbm.get_period()
            t = 0
            x = []
            y = []
            while t < period:
                r, _ = tbm.get_state_at_epoch(epoch.add_seconds(t))
                
                gst = get_eci_to_ecef_gst_angle(epoch.add_seconds(t))
                r = r.rotate_about_z(gst)
                r_lat_long = cartesian_to_spherical(r)
                long = Angle(r_lat_long.get_element(2), "radians").to_unit("degrees")
                x.append(long)
                alt = Distance(r.magnitude(), "meters").to_unit("kilometers")
                y.append(alt - 42164)
                t+=SECONDS_IN_MINUTE*5

            color = QtGui.QColor(0, 255, 0)
            self.available_sccs_table.item(row, 0).setBackground(color)
            self.available_sccs_table.item(row, 1).setBackground(color)

            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.active_sccs[scc] = self.rel_geo_plot.plot(
                x, 
                y, 
                pen = pg.mkPen(color=(r,g,b)), 
                name = name
                )

    def load_active_geo(self):
        self.tles  = TwoLineElsets.load_from_latest_active_geos()

        now = Epoch.from_timestamp(time.time())

        while self.available_sccs_table.rowCount() > 0:
            self.available_sccs_table.removeRow(0)

        for scc in sorted(self.tles.keys()):
            epoch, r, v, name  = self.tles[scc]
            row = self.available_sccs_table.rowCount()
            self.available_sccs_table.insertRow(row)
            scc_text = QtWidgets.QTableWidgetItem(scc)
            name_text = QtWidgets.QTableWidgetItem(name)
            self.available_sccs_table.setItem(row , 0, scc_text)
            self.available_sccs_table.setItem(row , 1, name_text)

            tbm = TwoBodyModel(r, v, epoch)
            r, v = tbm.get_state_at_epoch(now)
            self.tles[scc] = [now, r, v, name]

        print(len(self.tles.keys()), "TLEs loaded.")

def run():
    app = QtWidgets.QApplication(sys.argv)
    main = GeoWindow()
    main.show()
    sys.exit(app.exec_())
    