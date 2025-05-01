import win32com.client as win32
import os

class Aspen:
    def __init__(self):
        super().__init__()
        self.sims = []
        path = os.getcwd()
        self.simdir = os.path.join(path, "sim")
        self.message = ""
        self.lasterr = ""
        self.app1 = win32.GetObject(os.path.join(self.simdir,"DynamicsU407C2De.dynf"))
        self.sims.append(self.app1)
        self.OpenSimulationFile()
    
    def OpenSimulationFile(self):
        try:
            self.app1 = win32.GetObject(os.path.join(self.simdir,"DynamicsU407C2De.dynf"))
            # self.app2 = win32.GetObject(os.path.join(self.simdir,"DynamicsU407C2De.dynf"))
            self.message = "Simulation Openned"
            return True
        except:
            self.lasterr = "Cannot Open Simulation"
            return False
            

    def Visibling(self,state:bool):
        self.app1.Application.Visible = state
    
    def PauseSim(self):
        for simulation in self.sims:
            simulation.Pause()
        
    def RewindSim(self):
        for sim in self.sims:
            sim.Pause()
            sim.Application.Simulation.Results.Refresh()
            snapshots = sim.Results.SnapshotCount
            last_snapshot = sim.Results.GetSnapshot(snapshots - 1)
            print(type(snapshots))
            sim.Results.Rewind(last_snapshot)
        





import win32com.client as client


class AspenSimulatorManager:

    def __init__(self):
        self.simulations = []
        self.time_units = []
        self.time_coefficients = []
        self.delta_time = 0.000555
        path = os.getcwd()
        self.simdir = os.path.join(path, "sim")
        self.message = ""
        self.lasterr = ""
        self.app1 = win32.GetObject(os.path.join(self.simdir,"DynamicsU407C2De.dynf"))
        self.simulations.append(self.app1)
        self.is_main_loop_running = False

        # Load Aspen simulation files
        # for path in file_paths:
        #     self.simulations.append(client.GetObject(path))

        # Detect time units and set coefficients
        for simulation in self.simulations:
            unit = simulation.Application.Simulation.Options.TimeSettings.CommunicationUnits
            self.time_units.append(unit)

            if unit == "Hours":
                self.time_coefficients.append(1)
            elif unit == "Minutes":
                self.time_coefficients.append(1 / 60)
            elif unit == "Seconds":
                self.time_coefficients.append(1 / 3600)
            else:
                raise ValueError(f"Unknown time unit: {unit}")

    def get_last_message(self, simulation):
        last_index = simulation.Application.Simulation.OutputLogger.MessageCount - 1
        message = simulation.Application.Simulation.OutputLogger.Messages(last_index)
        print(message)
        return message

    def quit_all(self):
        for simulation in self.simulations:
            simulation.Application.Quit()

    def set_visibility(self, visible: bool):
        for simulation in self.simulations:
            simulation.Application.Visible = visible

    def interrupt_all(self, state: bool):
        for simulation in self.simulations:
            simulation.Interrupt(state)

    def pause_all(self):
        self.is_main_loop_running = False
        for simulation in self.simulations:
            simulation.Pause()

    def rewind_all(self):
        for simulation in self.simulations:
            simulation.Application.Simulation.Results.Refresh()
            snapshots = simulation.Results.SnapshotCount
            last_snapshot = simulation.Results.GetSnapshot(snapshots - 1)
            simulation.Results.Rewind(last_snapshot)
            self.get_last_message(simulation)

    def are_all_running(self):
        return all(sim.state == "Running" for sim in self.simulations)

    def are_all_paused_or_ready(self):
        return all(sim.state in ["Paused", "Ready"] for sim in self.simulations)

    def get_max_simulation_time(self):
        max_time = -1
        max_index = -1

        for index, simulation in enumerate(self.simulations):
            current_time = simulation.Time * self.time_coefficients[index]
            if current_time > max_time:
                max_time = current_time
                max_index = index

        return max_time, max_index

    def set_real_time_sync_factor(self, factor: float):
        for simulation in self.simulations:
            simulation.Application.Simulation.Options.TimeSettings.RealTimeSyncFactor = factor

    def run_all(self):
        if not self.are_all_paused_or_ready():
            return False

        for simulation in self.simulations:
            simulation.RunMode = "Dynamic"
            simulation.Run(False)

        self.is_main_loop_running = True
        loop_counter = 0

        while self.are_all_running() and self.is_main_loop_running:

            max_time, max_index = self.get_max_simulation_time()
            time_difference_detected = False

            for index, simulation in enumerate(self.simulations):
                current_time = simulation.Time * self.time_coefficients[index]
                if abs(current_time - max_time) > self.delta_time:
                    time_difference_detected = True
                    break

            loop_counter += 1
            if time_difference_detected:
                self.simulations[max_index].Pause()
                print(f"Paused simulation at index: {max_index} | Target Time: {max_time}")

                all_synced = False
                while not all_synced and self.is_main_loop_running:
                    all_synced = True
                    for index, simulation in enumerate(self.simulations):
                        current_time = simulation.Time * self.time_coefficients[index]
                        if abs(current_time - max_time) < self.delta_time:
                            simulation.Pause()
                        elif simulation.state != "Running":
                            print("Simulation solver failed.")
                            self.is_main_loop_running = False
                            return False
                        else:
                            all_synced = False

                if self.is_main_loop_running:
                    for simulation in self.simulations:
                        simulation.RunMode = "Dynamic"
                        simulation.Run(False)
                else:
                    break

                loop_counter = 0

            if loop_counter > 10:
                break

        return self.are_all_running()


if __name__ == "__main__":

    manager = Aspen()

    manager.set_visibility(True)
