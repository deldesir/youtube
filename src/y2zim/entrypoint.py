import argparse
import logging
import sys

from .constants import NAME, SCRAPER, YOUTUBE, logger
from .scraper import Y2zim


def main():
    parser = argparse.ArgumentParser(
        prog=NAME,
        description="Make ZIM off a Youtube collection",
    )
    parser.add_argument(
        "--id", help="Youtube ID of the collection",
        dest="youtube_id",
        default=None,
    )
    parser.add_argument(
        "--file", help="File containing Youtube videos IDs",
        dest="file",
        default=None,
    )
    parser.add_argument(
        "--name", help="Name of the project",
        required=True,
    )
    parser.add_argument(
        "--format",
        help="Format to download/transcode video to. webm is smaller",
        choices=["mp4", "webm"],
        default="webm",
        dest="video_format",
    )
    parser.add_argument(
        "--low-quality",
        help="Re-encode video using stronger compression",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--all-subtitles",
        help="Include auto-generated subtitles",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--pagination",
        help="Number of videos per page",
        type=int,
        dest="nb_videos_per_page",
        default=40,
    )
    parser.add_argument(
        "--autoplay",
        help="Enable autoplay on video articles (home never have autoplay). "
        "Behavior differs on platforms/browsers.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--output",
        help="Output folder for ZIM file",
        default="/output",
        dest="output_dir",
    )
    parser.add_argument(
        "--tmp-dir",
        help="Path to create temp folder in. Used for building ZIM file. "
        "Receives all data (storage space)",
    )
    parser.add_argument(
        "--no-zim",
        help="Don't produce a ZIM file, create HTML folder only.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--zim-file",
        help="ZIM file name (based on --name if not provided). "
        "If used, {period} is replaced with date as of YYYY-MM",
        dest="fname",
    )
    parser.add_argument(
        "--language", help="ISO-639-3 (3 chars) language code of content", default="eng"
    )
    parser.add_argument(
        "--locale",
        help="Locale name to use for translations (if avail) and time representations. "
        "Defaults to --language or English.",
        dest="locale_name",
    )
    parser.add_argument(
        "--title",
        help="Custom title for your project and ZIM. "
        "Default to Channel name (of first video if playlists)",
    )
    parser.add_argument(
        "--description",
        help="Custom description for your project and ZIM. "
        "Default to Channel name (of first video if playlists)",
    )
    parser.add_argument(
        "--creator",
        help="Name of content creator. Defaults to Channel name or “Youtue Channels”",
    )
    parser.add_argument(
        "--publisher", help="Custom publisher name (ZIM metadata)", default="Kiwix"
    )
    parser.add_argument(
        "--tags",
        help="List of comma-separated Tags for the ZIM file. "
        "_videos:yes added automatically",
        default="youtube",
    )
    parser.add_argument(
        "--profile",
        help="Custom profile image (path or URL). Squared. "
        "Will be resized to 100x100px",
        dest="profile_image",
    )
    parser.add_argument(
        "--banner",
        help="Custom banner image (path or URL). Will be resized to 1060x175px",
        dest="banner_image",
    )
    parser.add_argument(
        "--main-color",
        help="Custom color. Hex/HTML syntax (#DEDEDE). "
        "Default to main color of profile image.",
    )
    parser.add_argument(
        "--secondary-color",
        help="Custom secondary color. Hex/HTML syntax (#DEDEDE). "
        "Default to secondary color of profile image.",
    )
    parser.add_argument(
        "--debug",
        help="Enable verbose output",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--keep",
        help="Don't erase build folder on start (for debug/devel)",
        default=False,
        action="store_true",
        dest="keep_build_dir",
    )
    parser.add_argument(
        "--concurrency",
        help="Number of concurrent downloads",
        type=int,
        default=1,
        dest="max_concurrency",
    )
    parser.add_argument(
        "--version",
        help="Display scraper version and exit",
        action="version",
        version=SCRAPER,
    )
    parser.add_argument(
        "--dateafter",
        help="Custom filter to download videos uploaded on or after specified date. "
        "Format: YYYYMMDD or (now|today)[+-][0-9](day|week|month|year)(s)?",
    )
    parser.add_argument(
        "--optimization-cache",
        help="URL with credentials to S3 for using as optimization cache",
        dest="s3_url_with_credentials",
    )
    parser.add_argument(
        "--use-any-optimized-version",
        help="Use the cached files if present, whatever the version",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--custom-titles",
        nargs="+",
        help="Replace titles with custom titles from text files",
        default=False,
        dest="custom_titles",
    )
    args = parser.parse_args()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)


    try:
        if args.max_concurrency < 1:
            raise ValueError("Concurrency must be at least 1")  
        # Check for invalid values
        scraper = Y2zim(**dict(args._get_kwargs()), youtube_store=YOUTUBE)
        return scraper.run()
    except Exception as exc:
        logger.error(f"FAILED. An error occurred: {exc}")
        if args.debug:
            logger.exception(exc)
        return 1

if __name__ == "__main__":
    sys.exit(main())