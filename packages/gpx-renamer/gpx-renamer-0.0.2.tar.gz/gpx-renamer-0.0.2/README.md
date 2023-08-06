# gpx-renamer

File renamer for GPX traces


### Description

Small script to parse and rename GPX file based on its data like start date, recorded length, GPS bound coordinates, towns passed through (using offline reverse-geocode module).


### General workflow

    # move gpx files out of subdirectories (Like OSMTracker structure)
    mv */*.gpx .

    # delete empty folders
    find . -type d -delete

    # simulate renaming
    gpx-renamer-short -s *.gpx

    # rename for real
    gpx-renamer-short -r *.gpx


### CLI help


    usage: gpx-renamer [-h] [-c] [-d] [-f FORMAT] [-l] [-t] [-r] [-s] files [files ...]

    File renamer for GPX traces.

    positional arguments:
      files                 files to be processed

    optional arguments:
      -h, --help            show this help message and exit
      -c, --copy            copy instead of rename/move
      -d, --debug           activate debug output, can be used to see all Format keywords
      -f FORMAT, --format FORMAT
                            use custom format
      -l, --long            use long format for name: {startdate}-{starttime}_{minlat},{minlon}-{maxlat},{maxlon}_{cities}_{length}_{points}
      -t, --short           use short format for name: {startdate}-{starttime}_{minlat},{minlon}-{maxlat},{maxlon}_{edges}_{length}
      -r, --rename          rename, defaut is using minimum format: {startdate}-{starttime}_{edges}
      -s, --simulate        dry run

    Helper proxies: gpx-renamer-min same as using -r, gpx-renamer-short same as using -r -t, gpx-renamer-long same as using -r -l


### Why need such tool?

- When using multiple recording devices, each has its own trace naming convension. Seems more effective to keep file in chronical order. Ex: `YYYYMMDD` is sortable better than other date formats.
- Categorize GPX based on covered location (city, town, geocode) in automated way.
- Easier to tag when uploading to Open Street Map OSM.


### Dependencies

- `gpxpy`  
- `reverse-geocode`


### Installation from source

    #day1
    pip3 install -q build

    #day2
    python3 -m build
    pip3 install dist/gpx-renamer-0.0.1.tar.gz


### PyPI upload new modified source

    #day1
    pip3 install twine

    #day2
    twine upload dist/*

### Related Resources


- [Best practices file naming](https://library.stanford.edu/research/data-management-services/data-best-practices/best-practices-file-naming)


### Useful tools

- [Validation](https://www.topografix.com/gpx_validation.asp)

        saxcount -v=always -n -s -f file.gpx

- Validation using `gpxpy`

        gpxinfo file.gpx

- Split tracks using `gpxutils`

        gpxclean -n -s 1000 file.gpx

- Generate map using `papermap`

        papermap -sc 10000 wgs84 36.78189 5.90056 Taher.pdf`

- Splice and clean GPX using GPSPrune (GUI tool)