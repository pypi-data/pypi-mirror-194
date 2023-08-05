import inspect
import logging
import os.path
import sys
import humanfriendly
import datetime

import boto3
import click
import pytz
from rich.console import Console
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(console=Console(stderr=True))],
)
log = logging.getLogger("rich")
log.setLevel(logging.INFO)

sys.path.append(
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django

django.setup()

from preservationdatabase.models import (
    CarinianaPreservation,
    ClockssPreservation,
    HathiPreservation,
    InternetArchivePreservation,
    LockssPreservation,
    OculScholarsPortalPreservation,
    PKPPreservation,
    PorticoPreservation,
    LastFill,
    ISSN,
    ISSNL,
)

from django.db import transaction
import utils


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--url",
    default="https://api.portico.org/kbart/Portico_Holding_KBart.txt",
    help="The URL to fetch",
)
@click.option("--local", is_flag=True, default=False)
@transaction.atomic()
def import_portico(url, local):
    """Download and import data from Portico"""
    PorticoPreservation.import_data(url, local=local)


@click.command()
@click.option(
    "--file",
    default="ia_sim_keepers_kbart.2022-12-12.tsv",
    help="The filename of the Hathitrust full dump to use",
)
@click.option(
    "--bucket",
    default="preservation.research.crossref.org",
    help="The s3 bucket from which to retrieve the data",
)
@click.option("--local", is_flag=True, default=False)
@transaction.atomic()
def import_internet_archive(file, bucket, local):
    """Import data from Hathi (requires local file download or S3)"""
    s3client = boto3.client("s3")
    InternetArchivePreservation.import_data(
        file, bucket=bucket, s3client=s3client, local=local
    )


@click.command()
@click.option(
    "--url",
    default="https://reports.clockss.org/keepers/keepers-CLOCKSS-report.csv",
    help="The URL to fetch",
)
@click.option("--local", is_flag=True, default=False)
@transaction.atomic()
def import_clockss(url, local):
    """Download and import data from CLOCKSS"""
    ClockssPreservation.import_data(url, local=local)


@click.command()
@click.option(
    "--url",
    default="https://reports.lockss.org/keepers/keepers-LOCKSS-report.csv",
    help="The URL to fetch",
)
@click.option("--local", is_flag=True, default=False)
@transaction.atomic()
def import_lockss(url, local):
    """Download and import data from LOCKSS"""
    LockssPreservation.import_data(url, local=local)


@click.command()
@click.option(
    "--url",
    default="https://pkp.sfu.ca/files/pkppn/onix.csv",
    help="The URL to fetch",
)
@click.option("--local", is_flag=True, default=False)
@transaction.atomic()
def import_pkp(url, local):
    """Download and import data from PKP's private LOCKSS network"""
    PKPPreservation.import_data(url, local=local)


@click.command()
@click.option(
    "--url",
    default="http://reports-lockss.ibict.br/keepers/pln/ibictpln/keepers-IBICTPLN-report.csv",
    help="The URL to fetch",
)
@click.option("--local", is_flag=True, default=False)
@transaction.atomic()
def import_cariniana(url, local):
    """Download and import data from Cariniana"""
    CarinianaPreservation.import_data(url, local=local)


@click.command()
@click.option(
    "--file",
    default="hathi_full_20230101.txt",
    help="The filename of the Hathitrust full dump to use",
)
@click.option(
    "--bucket",
    default="preservation.research.crossref.org",
    help="The s3 bucket from which to retrieve the data",
)
@click.option("--local", is_flag=True, default=False)
@transaction.atomic()
def import_hathi(file, bucket, local):
    """Import data from Hathi (requires local file download or S3)"""
    s3client = boto3.client("s3")
    HathiPreservation.import_data(
        file, bucket=bucket, s3client=s3client, local=local
    )


@click.command()
@click.option(
    "--file",
    default="scholars_portal_keepers_20230202.xml",
    help="The filename of the OCUL full dump to use",
)
@click.option(
    "--bucket",
    default="preservation.research.crossref.org",
    help="The s3 bucket from which to retrieve the data",
)
@transaction.atomic()
def import_ocul(file, bucket):
    """Import data from Ocul (requires local file download or S3)"""

    s3client = boto3.client("s3")
    OculScholarsPortalPreservation.import_data(
        file, bucket=bucket, s3client=s3client
    )

    return


@click.command()
@transaction.atomic()
def stamp_cache_today():
    """Mark the latest imports as today"""
    from preservationdatabase.constants import archives

    for key, value in archives.items():
        LastFill.set_last_fill(value.name())


@click.command()
@transaction.atomic()
def clear_cache():
    """Clear the import cache"""
    LastFill.clear()


@click.command()
@click.argument("issnl_file")
@transaction.atomic()
def import_issnl(issnl_file):
    """Import ISSN-L mappings"""
    utils.import_issnl(issnl_file, ISSNL, ISSN)


@click.command()
@transaction.atomic()
def show_cache():
    """Show last fill date/times and cache status"""

    for lf in LastFill.objects.all():
        logging.info(lf)
        time_delta = datetime.datetime.now(pytz.utc) - lf.last_fill_date
        logging.info(
            "Last cache stamp for {} was {}".format(
                lf.archive_name,
                humanfriendly.format_timespan(
                    humanfriendly.coerce_seconds(time_delta)
                ),
            )
        )

        if lf.cache_valid:
            logging.info("{} will use cached version".format(lf.archive_name))
        else:
            logging.info(
                "{} will be fetched from source".format(lf.archive_name)
            )


@click.command()
@transaction.atomic()
def show_archives():
    """Clear the import cache"""
    from constants import archives

    for key, value in archives.items():
        logging.info(value.name())


@click.command()
@click.argument("issn")
@transaction.atomic()
def show_issn(issn):
    """Show preservation items that match an ISSN"""
    from constants import archives

    for key, archive_object in archives.items():
        issns = archive_object.objects.filter(issn=issn)

        for issn_object in issns:
            logging.info(f"{archive_object.name()} preserves {issn_object}")

        if "eissn" in archive_object._meta.get_fields():
            issns = archive_object.objects.filter(eissn=issn)

            for issn_object in issns:
                logging.info(f"{archive_object.name()} preserves {issn_object}")


@click.command()
@click.argument("archive_name")
@click.option("--count", default=25, help="Give random samples for an archive")
@click.option(
    "--only-crossref",
    help="Only return Crossref titles",
    is_flag=True,
    default=False,
)
@transaction.atomic()
def random_samples(archive_name, count, only_crossref):
    """Return random samples that occur in and out of an archive"""
    from constants import archives
    from crossref.restful import Etiquette, Journals
    import utils

    archive = None

    for key, archive_object in archives.items():
        if archive_object.name() == archive_name:
            archive = archive_object

    if not archive:
        log.error(f"Archive {archive_name} not found")
        return

    random_entries = utils.random_db_entries(
        archive, count, only_crossref=only_crossref
    )
    not_in_archive = []

    my_etiquette = Etiquette(
        "Preservation Status", "0.01", "https://eve.gd", "meve@crossref.org"
    )

    jrnls = Journals(etiquette=my_etiquette)

    # now find entries that are not in the archive:
    while len(not_in_archive) < count - 1:
        for key, other_archive in archives.items():
            if other_archive != archive:
                other_entries = utils.random_db_entries(other_archive, count)

                for entry in other_entries:
                    if not utils.in_archive(entry, archive):
                        if only_crossref:
                            append = False

                            new_issns = utils.expand_issns([entry.issn])

                            for issn in new_issns:
                                jrnl = jrnls.journal(issn=issn)

                                if jrnl:
                                    append = True
                                    break

                            if hasattr(entry, "eissn"):
                                new_eissns = utils.expand_issns([entry.eissn])

                                for issn in new_eissns:
                                    jrnl = jrnls.journal(issn=issn)

                                    if jrnl:
                                        append = True
                                        break

                            if append:
                                not_in_archive.append(entry)
                                print(
                                    "Found not-in-archive crossref entry ({}): {}".format(
                                        len(not_in_archive), entry
                                    )
                                )
                        else:
                            not_in_archive.append(entry)

                        if len(not_in_archive) == count - 1:
                            break

            if len(not_in_archive) == count - 1:
                break

    for entry in random_entries:
        logging.info("{} contains: {}".format(archive_name, entry))

    for entry in not_in_archive:
        logging.info("{} does not contain: {}".format(archive_name, entry))


@click.command()
def import_all():
    """Download and import all data (excluding HathiTrust)"""

    import_clockss(
        url="https://reports.clockss.org/keepers/keepers-CLOCKSS-report.csv"
    )

    import_portico(
        url="https://api.portico.org/kbart/Portico_Holding_KBart.txt"
    )

    import_lockss(
        url="https://reports.lockss.org/keepers/keepers-LOCKSS-report.csv"
    )

    import_cariniana(
        url="http://reports-lockss.ibict.br/keepers/pln/ibictpln/keepers-IBICTPLN-report.csv"
    )


@click.command()
@click.argument("doi")
@click.option(
    "--literal", help="Use literal DOI (no schema)", is_flag=True, default=False
)
@click.option(
    "--no-issn", help="Do not expand ISSN list", is_flag=True, default=False
)
def show_preservation(doi, literal=False, no_issn=False):
    """
    Determine whether a DOI is preserved
    """
    if not literal:
        doi = utils.normalize_doi(doi)

    preservation_statuses, doi = utils.show_preservation_for_doi(
        doi, no_issn=no_issn
    )

    for key, value in preservation_statuses.items():
        preserved, done = value

        if preserved:
            if done:
                log.info(
                    f"[green]Preserved:[/] in {key}", extra={"markup": True}
                )
            else:
                log.info(
                    f"[yellow]Preserved (in progress):[/] " f"in {key}",
                    extra={"markup": True},
                )
        else:
            log.info(f"[red]Not preserved:[/] in {key}", extra={"markup": True})


if __name__ == "__main__":
    cli.add_command(clear_cache)
    cli.add_command(import_all)
    cli.add_command(import_cariniana)
    cli.add_command(import_clockss)
    cli.add_command(import_hathi)
    cli.add_command(import_internet_archive)
    cli.add_command(import_issnl)
    cli.add_command(import_lockss)
    cli.add_command(import_ocul)
    cli.add_command(import_pkp)
    cli.add_command(import_portico)
    cli.add_command(random_samples)
    cli.add_command(show_archives)
    cli.add_command(show_cache)
    cli.add_command(show_issn)
    cli.add_command(show_preservation)
    cli.add_command(stamp_cache_today)
    cli()
