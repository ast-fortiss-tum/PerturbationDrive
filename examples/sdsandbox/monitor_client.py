#!/usr/bin/env python
"""
Predict Client
Create a client to accept image inputs and run them against a trained neural network.
This then sends the steering output back to the server.

`python3 examples/sdsandbox/monitor_client.py --model=./examples/sdsandbox/mymodel.h5`
`python3 examples/sdsandbox/monitor_client.py --model=./examples/sdsandbox/mymodel.h5 --perturbation=dynamic_rain_filter`
`python3 examples/sdsandbox/monitor_client.py --model=./examples/sdsandbox/mymodel.h5 --perturbation=defocus_blur --perturbation=increase_brightness --perturbation=pixelate --perturbation=contrast`
`python3 examples/sdsandbox/monitor_client.py --model=./examples/sdsandbox/mymodel.h5 --perturbation=dynamic_smoke_filter --perturbation=dynamic_lightning_filter --perturbation=dynamic_sun_filter --perturbation=dynamic_object_overlay`
Author: Tawn Kramer
"""
from __future__ import print_function
import argparse
import pygame
import conf
import predict_client

pygame.init()
ch, row, col = conf.ch, conf.row, conf.col

size = (col * 2, row * 2)
pygame.display.set_caption("sdsandbox data monitor")
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)
camera_surface = pygame.surface.Surface((col, row), 0, 24).convert()
myfont = pygame.font.SysFont("monospace", 15)


def screen_print(x, y, msg, screen):
    label = myfont.render(msg, 1, (255, 255, 0))
    screen.blit(label, (x, y))


def display_img(img, steering):
    img = img.swapaxes(0, 1)
    # draw frame

    pygame.surfarray.blit_array(camera_surface, img)
    camera_surface_2x = pygame.transform.scale2x(camera_surface)
    screen.blit(camera_surface_2x, (0, 0))
    # steering value
    screen_print(10, 10, "NN    :" + str(steering), screen)
    pygame.display.flip()


if __name__ == "__main__":
    """Before using this method make sure to set the correct camera size in conf.py"""
    parser = argparse.ArgumentParser(description="prediction server with monitor")
    parser.add_argument("--model", type=str, help="model name. no json or keras.")
    parser.add_argument(
        "--perturbation",
        dest="perturbation",
        action="append",
        type=str,
        default=[],
        help="perturbations to use on the model. by default all are used",
    )
    args = parser.parse_args()

    address = ("127.0.0.1", 9091)

    try:
        predict_client.go(
            args.model, address, constant_throttle=0.3, image_cb=display_img, pert_funcs=args.perturbation
        )
    except KeyboardInterrupt:
        print("got ctrl+c break")
