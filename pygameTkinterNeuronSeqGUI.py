import pygame
import networkx as nx
import math
import numpy as np
import tkinter as tk
import neuronSeq2 as ns
import threading
import time

neuronSeq = ns.NeuronSeq()
G = ns.NetworkGraph(neuronSeq)
n = G.add_nnote(midi_channel=2, note=60, duration=0.5, id="A", velocity=100)
n.set_activation_function(1)
n = G.add_nnote(midi_channel=2, note=62, duration=0.5, id="B", velocity=100)
n.set_activation_function(1)
n = G.add_nnote(midi_channel=2, note=64, duration=0.5, id="C", velocity=100)
n.set_activation_function(1)
n = G.add_nnote(midi_channel=2, note=65, duration=0.5, id="D", velocity=100)
n.set_activation_function(1)
n = G.add_nnote(midi_channel=2, note=67, duration=0.5, id="E", velocity=100)
n.set_activation_function(1)

G.add_connection("A->B", 0, 1, 156, 156)
G.add_connection("B->C", 1, 2, 156, 156)
G.add_connection("C->D", 2, 3, 156, 156)
G.add_connection("D->E", 3, 4, 156, 156)
G.add_connection("E->A", 4, 0, 156, 156)


def print_neuronSeq_nnotes():
    for nnote in neuronSeq.nnotes:
        print(nnote.id, nnote.channel, nnote.note, nnote.velocity, nnote.duration)
    return

def print_neuronSeq_connections():
    for connection in neuronSeq.connections:
        print(connection.name, connection.source, connection.destination, connection.weight_0_to_1, connection.weight_1_to_0)
    return

class AddNeuronWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Neuron")
        self.geometry("300x300")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.create_widgets()

    def close_window(self):
        self.destroy()

    def create_widgets(self):
        self.neuron_name_label = tk.Label(self, text="Neuron Name")
        self.neuron_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.neuron_name_entry = tk.Entry(self)
        self.neuron_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.midi_channel_label = tk.Label(self, text="MIDI Channel")
        self.midi_channel_label.grid(row=1, column=0, padx=10, pady=10)
        self.midi_channel_entry = tk.Entry(self)
        self.midi_channel_entry.grid(row=1, column=1, padx=10, pady=10)
        self.midi_note_label = tk.Label(self, text="MIDI Note")
        self.midi_note_label.grid(row=2, column=0, padx=10, pady=10)
        self.midi_note_entry = tk.Entry(self)
        self.midi_note_entry.grid(row=2, column=1, padx=10, pady=10)
        self.velocity_label = tk.Label(self, text="Velocity")
        self.velocity_label.grid(row=3, column=0, padx=10, pady=10)
        self.velocity_entry = tk.Entry(self)
        self.velocity_entry.grid(row=3, column=1, padx=10, pady=10)
        self.duration_label = tk.Label(self, text="Duration")
        self.duration_label.grid(row=4, column=0, padx=10, pady=10)
        self.duration_entry = tk.Entry(self)
        self.duration_entry.grid(row=4, column=1, padx=10, pady=10)
        self.add_button = tk.Button(self, text="Add", command=self.add_neuron)
        self.add_button.grid(row=5, column=0, padx=10, pady=10)
        
    def add_neuron(self):
        global G, pos, DVpos
        neuron_name = self.neuron_name_entry.get()
        midi_channel = int(self.midi_channel_entry.get())
        midi_note = int(self.midi_note_entry.get())
        velocity = int(self.velocity_entry.get())
        duration = float(self.duration_entry.get())
        G.add_nnote(midi_channel=midi_channel, note=midi_note, duration=duration, id=neuron_name, velocity=velocity)
        pos = nx.spring_layout(G)
        DVpos={}
        for node in G.nodes():
            DVpos[node] = DistanceVector(pos[node])
        print_neuronSeq_nnotes()
        return
    
class AddConnectionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Connection")
        self.geometry("300x300")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.create_widgets()

    def close_window(self):
        self.destroy()

    def create_widgets(self):
        connection_name_label = tk.Label(self, text="Connection Name")
        connection_name_label.grid(row=0, column=0, padx=10, pady=10)
        self.connection_name_entry = tk.Entry(self)
        self.connection_name_entry.grid(row=0, column=1, padx=10, pady=10)
        source_label = tk.Label(self, text="Source")
        source_label.grid(row=1, column=0, padx=10, pady=10)
        self.source_entry = tk.Entry(self)
        self.source_entry.grid(row=1, column=1, padx=10, pady=10)
        target_label = tk.Label(self, text="Target")
        target_label.grid(row=2, column=0, padx=10, pady=10)
        self.target_entry = tk.Entry(self)
        self.target_entry.grid(row=2, column=1, padx=10, pady=10)
        self.weight0_label = tk.Label(self, text="Weight 0")
        self.weight0_label.grid(row=3, column=0, padx=10, pady=10)
        self.weight0_entry = tk.Entry(self)
        self.weight0_entry.grid(row=3, column=1, padx=10, pady=10)
        self.weight1_label = tk.Label(self, text="Weight 1")
        self.weight1_label.grid(row=4, column=0, padx=10, pady=10)
        self.weight1_entry = tk.Entry(self)
        self.weight1_entry.grid(row=4, column=1, padx=10, pady=10)
        self.add_connection_button = tk.Button(self, text="Add", command=self.add_connection)
        self.add_connection_button.grid(row=5, column=0, padx=10, pady=10)

    def add_connection(self):
        global G, pos, DVpos
        connection_name = self.connection_name_entry.get()
        source = int(self.source_entry.get())
        target = int(self.target_entry.get())
        weight0 = float(self.weight0_entry.get())
        weight1 = float(self.weight1_entry.get())
        G.add_connection(connection_name, source, target, weight0, weight1)
        pos = nx.spring_layout(G)
        DVpos={}
        for node in G.nodes():
            DVpos[node] = DistanceVector(pos[node])
        print_neuronSeq_connections()
        return
    
neuronSeq_window = tk.Tk()
neuronSeq_window.title("NeuronSeq")
neuronSeq_window.geometry("300x300")
neuronSeq_window.resizable(True, True)
neuronSeq_window.protocol("WM_DELETE_WINDOW", neuronSeq_window.destroy)

addNeuronWindow = AddNeuronWindow(neuronSeq_window)
addConnectionWindow = AddConnectionWindow(neuronSeq_window)

def get_angle(direction=1, angle=1):
    new_angle = angle * 30 * direction
    return new_angle%360

class DistanceVector():
    def __init__(self, nx_point):
        angle = 1
        direction = 1
        self.nx_point = nx_point
        self.angle = get_angle(direction, angle)
        self.update_nx_point()

    def change_angle_x(self, angle):
        self.angle = angle
        return self.update_nx_point()
    
    def change_angle_y(self, angle):
        self.angle = angle
        return self.update_nx_point()

    def update_nx_point(self):
        x, y = self.nx_point
        #𝑥′=𝑥cos𝜃−𝑦sin𝜃
        #𝑦′=𝑥sin𝜃+𝑦cos𝜃
        new_x = x * math.cos(self.angle) + y * math.sin(self.angle)
        new_y = x * math.sin(self.angle) - y * math.cos(self.angle)

        self.vector_length = math.sqrt((new_x - x)**2 + (new_y - y)**2)
        self.nx_point = (new_x, new_y)
        return self
        
    def get_coordinates(self):
        return self.nx_point
    
# Define rotation functions
def rotate_x(distance_vector, rotation_angle):
    distance_vector = distance_vector.change_angle_x(rotation_angle)
    return distance_vector

def rotate_y(distance_vector, rotation_angle):
    distance_vector = distance_vector.change_angle_y(rotation_angle)
    return distance_vector
    
# Initialize Pygame
pygame.init()

# Set window dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("NeuronSeq network")
running = True

# Define a layout for the nodes
pos = nx.spring_layout(G)
DVpos={}
for node in G.nodes():
    DVpos[node] = DistanceVector(pos[node])

def run_network_window(event):
    global running
    if running == False:
        return

    # Variables for handling tilting, zooming, and panning
    # Move zoom_factor and pan_offset to global
    global zoom_factor
    global pan_offset
    
    # Handle events
    if event.type == pygame.QUIT:
        running = False
        return
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_PLUS:
            zoom_factor += 10.0
        elif event.key == pygame.K_MINUS:
            zoom_factor -= 10.0
        elif event.key == pygame.K_LEFT:
            pan_offset[0] -= 20
        elif event.key == pygame.K_RIGHT:
            pan_offset[0] += 20
        elif event.key == pygame.K_UP:
            pan_offset[1] -= 20
        elif event.key == pygame.K_DOWN:
            pan_offset[1] += 20
        elif event.key == pygame.K_ESCAPE:
            running = False
            return
        
        elif event.key == pygame.K_r:
            for node in G.nodes():
                DVpos[node] = rotate_x(DVpos[node], DVpos[node].angle+0.1)
        elif event.key == pygame.K_t:
            for node in G.nodes():
                DVpos[node] = rotate_x(DVpos[node], DVpos[node].angle-0.1)
        elif event.key == pygame.K_f:
            for node in G.nodes():
                DVpos[node] = rotate_y(DVpos[node], DVpos[node].angle+0.1)
        elif event.key == pygame.K_g:
            for node in G.nodes():
                DVpos[node] = rotate_y(DVpos[node], DVpos[node].angle-0.1)

    # Clear screen
    screen.fill((255, 255, 255))

    # Draw edges and nodes
    for edge in G.edges():
        color = (0, 0, 0)
        r = np.random.randint(0,255,1)
        g = np.random.randint(0,255,1)
        b = np.random.randint(0,255,1)
        color = (r,g,b)
        # Scale and apply pan offset and zoom factor
        x1, y1 = DVpos[edge[0]].get_coordinates()
        x2, y2 = DVpos[edge[1]].get_coordinates()
        x1 = x1 * zoom_factor + width / 2 + pan_offset[0]
        y1 = y1 * zoom_factor + height / 2 + pan_offset[1]
        x2 = x2 * zoom_factor + width / 2 + pan_offset[0]
        y2 = y2 * zoom_factor + height / 2 + pan_offset[1]
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)

    # Draw nodes
    for node in G.nodes():
        x, y = DVpos[node].get_coordinates()
        x = x * zoom_factor + width / 2 + pan_offset[0]
        y = y * zoom_factor + height / 2 + pan_offset[1]
        pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), 12)
    
    pygame.display.update()

    return

def main():
    global zoom_factor
    global pan_offset

    while running:
        event = pygame.event.poll()
        neuronSeq_window.update()
        run_network_window(event)
        #time.sleep(0.1)
    return

if __name__ == "__main__":
    zoom_factor = 100.0  # Initial zoom factor
    pan_offset = [0, 0]  # Initial pan offset
    main()

# Quit Pygame
pygame.quit()
