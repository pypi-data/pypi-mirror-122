# gpx-renamer

File renamer for GPX traces


### Description

Small script to parse and rename GPX file based on its data like start date, recorded length, GPS bound coordinates, towns passed through (using offline reverse-geocode module).

### Why?

- When using multiple recording devices, each has its own trace naming convension. Seems more effective to keep file in chronical order. Ex: `YYYYMMDD` is sortable better than other date formats.
- Categorize GPX based on covered location (city, town, geocode) in automated way.
- Easier to tag when uploading to Open Street Map OSM.





### Dependencies

- [`gpxpy`](https://pypi.org/project/gpxpy/)
    `gpxinfo file.gpx`
- `reverse-geocode`


### Installation

pip3 install -q build
python3 -m build
pip3 install dist/gpx-renamer-0.0.1.tar.gz

### Related Resources


- https://library.stanford.edu/research/data-management-services/data-best-practices/best-practices-file-naming


### Useful tools

- https://www.topografix.com/gpx_validation.asp

    validation

    `saxcount -v=always -n -s -f file.gpx`

- https://github.com/emenendez/gpxutils

    split tracks

    `gpxclean -n -s 1000 file.gpx`

- papermap

    `papermap -sc 10000 wgs84 36.78189 5.90056 Taher.pdf`

- gpsprune