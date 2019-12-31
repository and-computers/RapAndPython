#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script for creating heatmap of artists geography
"""
from gmplot import gmplot

US_CENTER_LAT = 39.8283
US_CENTER_LNG = -98.5795
HTMLFILE = '127-heatmap.html'

# TODO: replace w/ geocodes
# lat, lng = mymap.geocode("Stanford University")
LosAngeles = (34.0522, -118.2437, "West Coast")
NewYork = (40.7128, -74.006, "East Coast")
Chicago = (41.8781, -87.6298, "Midwest")
Oakland = (37.8044, -122.2712, "West Coast")
Atlanta = (33.7490, -84.3880, "Southern")
WashDC = (38.9072, -77.0369, "East Coast")
Miami = (25.7617, -80.1918, "Southern")
Charlotte = (35.2271, -80.8431, "Southern")
Toronto = (43.6532, -79.3832, "Canada")
Philadelphia = (39.9526, -75.1652, "East Coast")
STL = (38.627, -90.1994, "Southern")
Memphis = (35.1495, -90.0490, "Southern")
Houston = (29.7604, -95.3698, "Southern")
Tappahannock = (37.9244, -76.8591, "Southern")
SanMarcos = (29.883, -97.9414, "Southern")
Tallahassee = (30.4383, -84.2807, "Southern")
London = (51.5074, 0.1278, "UK")
Jamaica = (18.1096, -77.2975, "Caribbean")
Lagos = (6.5244, 3.3792, "West Africa")
MobileAlabama = (30.6954, -88.0399, "Southern")
Oshawa = (43.8971, -78.8658, "Canada")
Portland = (45.5051, -122.6750, "West Coast")
Clearwater = (27.9659, -82.8001, "Southern")  # FL
PompanoBeach = (26.2379, -80.1248, "Southern")  # FL
Detroit = (42.3314, -83.0458, "Midwest")
Tupelo = (34.2576, -88.7034, "Southern")  # MS
Nola = (29.9511, -90.0715, "Southern")
Louisville = (38.2527, -85.7585, "Southern")
Grapevine = (32.9343, -97.0781, "Southern")  # TX
Petersburg = (37.2279, -77.4019, "Southern")  # VA

artist_locale = {
    'H.E.R.':
    Oakland,
    'YG':
    LosAngeles,
    'Wale':
    WashDC,
    'Jeremih':
    Chicago,
    'Layton Greene':
    STL,
    'Lil Baby': Atlanta,
    'City Girls':
    Miami,
    'PnB Rock':
    Philadelphia,
    'Yo Gotti':
    Memphis,
    'Lil Baby':
    Atlanta,
    '21 Savage':
    Atlanta,
    'Sheck Wes':
    NewYork,
    'DaBaby':
    Charlotte,
    'Shordie Shordie':
    WashDC,
    'Megan Thee Stallion':
    Houston,
    'Mustard':
    LosAngeles,
    'Roddy Ricch':
    LosAngeles,
    'Young Thug':
    Atlanta,
    'Gunna':
    Atlanta,
    'Gunna':
    Atlanta,
    "Derez De’Shon":
    Atlanta,
    'Chris Brown':
    Tappahannock,
    'Drake':
    Toronto,
    'Ella Mai':
    London,
    'Tha Dogg Pound':
    LosAngeles,
    'Soulja Boy':
    Atlanta,
    'Gucci Mane':
    Atlanta,
    'Shawty Lo':
    Atlanta,
    'Bino Rideaux':
    LosAngeles,
    'YG':
    LosAngeles,
    'DJ Quik':
    LosAngeles,
    'Roddy Ricch':
    LosAngeles,
    'BROCKHAMPTON':
    SanMarcos,
    'Post Malone': Grapevine,
    'Quavo':
    Atlanta,
    'Leven Kali':
    LosAngeles,
    'Syd':
    LosAngeles,
    'Afro B':
    London,
    'Beyoncé':
    Houston,
    'Koffee':
    Jamaica,
    'Rich Boy':
    MobileAlabama,
    'Polow Da Don':
    Clearwater,
    'Rocko':
    Atlanta,
    'Meek Mill':
    Philadelphia,
    'Ella Mai':
    London,
    'Tory Lanez':
    Toronto,
    'T - Pain':
    Tallahassee,
    'YG':
    LosAngeles,
    'Drake':
    Toronto,
    'Kamaiyah':
    Oakland,
    'Thundercat': LosAngeles,
    'Rick Ross':
    Miami,
    'Drake':
    Toronto,
    'The Internet':
    LosAngeles,
    'Burna Boy': Lagos,
    'G - Eazy':
    Oakland,
    'Blueface':
    LosAngeles,
    'ALLBLACK':
    Portland,
    'YG':
    LosAngeles,
    'BROCKHAMPTON':
    SanMarcos,
    'Drake':
    Toronto,
    'Young Thug':
    Atlanta,
    'J. Cole':
    Charlotte,
    'Travis Scott':
    Houston,
    'Free Nationals':
    LosAngeles,
    'Daniel Caesar':
    Oshawa,
    'Unknown Mortal Orchestra':
    Portland,
    'Kodak Black': PompanoBeach,
    'Offset':
        Atlanta,
    'Travis Scott':
    Houston,
    'DaVido': Lagos,
    "Lil' Mo": NewYork,
    "Fabolous":
    NewYork,
    'Daniel Caesar':
    Oshawa,
    'Sleepy Brown': Atlanta,
    'OutKast':
    Atlanta,
    'YG':
    LosAngeles,
    'Teefli': LosAngeles,
    '2 Chainz':
    Atlanta,
    'Ty Dolla $ign':
    LosAngeles,
    'Trey Songz': Petersburg,
    'Jhené Aiko':
        LosAngeles,
    'Santi': Lagos,
    'GoldLink': WashDC,
    'Gucci Mane':
    Atlanta,
    'Bryson Tiller': Louisville,
    'LION BABE': NewYork,
    'Lil Nas X': Atlanta,
    'DaBaby':
    Charlotte,
    'Junior M.A.F.I.A.': NewYork,
    'QUIN': LosAngeles,
    '6LACK':
    Atlanta,
    'SiR':
    LosAngeles,
    'Chance the Rapper':
    Chicago,
    'Alex Wiley': Chicago,
    'Akenya': Chicago,
    'E - 40':
    Oakland,
    'Tha Eastsidaz':
    LosAngeles,
    'Butch Cassidy':
    LosAngeles,
    'Kamaiyah':
    Oakland,
    'Snoop Dogg':
    LosAngeles,
    'UGK':
    Houston,
    'OutKast':
    Atlanta,
    'Summer Walker':
    Atlanta,
    'Usher':
    Atlanta,
    'Bryson Tiller': Louisville,
    'Jacquees':
    Atlanta,
    'Megan Thee Stallion':
    Houston,
    'DaBaby':
    Charlotte,
    'Doja Cat': LosAngeles,
    'Tyga':
    LosAngeles,
    'NAV': Toronto,
    'Meek Mill': Philadelphia,
    'James Fauntleroy': LosAngeles,
    'Swae Lee': Tupelo,
    'TWENTY88': Detroit,
    'Nipsey Hussle':
    LosAngeles,
    'Kanye West':
    Chicago,
    'Lil Wayne': Nola,
    'JAY - Z':
    NewYork,
    'Kanye West':
    Chicago
}


def get_google_map_creds(fname='heatmap/gmaps-creds.txt'):
    """
    get google maps credentials for api access
    """

    with open(fname) as f_h:
        creds = f_h.read()
    return creds


def main():
    plotter = gmplot.GoogleMapPlotter(
        center_lat=US_CENTER_LAT,
        center_lng=US_CENTER_LNG,
        zoom=1,
        apikey=get_google_map_creds())

    lats = []
    lngs = []

    counts = {}

    for artist, coords in artist_locale.items():

        lats.append(coords[0])
        lngs.append(coords[1])

        if coords[2] in counts:
            counts[coords[2]] += 1
        else:
            counts[coords[2]] = 1

    plotter.heatmap(lats=lats, lngs=lngs)

    print(counts)

    plotter.draw(HTMLFILE)

if __name__ == "__main__":
    main()
