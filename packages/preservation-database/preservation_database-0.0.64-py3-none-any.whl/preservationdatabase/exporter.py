import json
import logging
from datetime import date
from typing import DefaultDict, Any


def get_members(s3client, samples_bucket, samples_path) -> list[str]:
    """
    Retrieves the list of members from the S3 bucket
    :param s3client: the s3client object to use to fetch
    :param samples_bucket: the name of the samples bucket
    :param samples_path: the path of the samples object
    :return: a list of strings of member IDs
    """

    # the samples research bucket contains JSON-L with the filename
    # schema member-1.jsonl etc.
    # Note also: we use S3 for this so that we definitely know what
    # files are available, rather than the REST API (in case there is
    # a bug in the sampling framework that leads to an unavailable
    # object)

    import re

    r = re.compile(r"member-(\d+).jsonl")
    return [
        m.group(1)
        for m in map(
            r.match,
            list_bucket(
                s3client,
                samples_bucket=samples_bucket,
                samples_path=samples_path,
            ),
        )
        if m is not None
    ]


def list_bucket(s3client, samples_bucket, samples_path) -> list[str]:
    """
    Lists the contents of the samples bucket
    :param s3client: the s3client object to use to fetch
    :param samples_bucket: the name of the samples bucket
    :param samples_path: the path of the samples object
    :return: a list of object names
    """

    paginator = s3client.get_paginator("list_objects_v2")
    member_list = []

    for page in paginator.paginate(
        Bucket=samples_bucket, Prefix=f"{samples_path}"
    ):
        for obj in page["Contents"]:
            filename = obj["Key"]
            member_list.append(filename.split("/")[-1])

    return member_list


def get_samples(s3client, member_id, samples_bucket, samples_path) -> list:
    """
    Retrieves the list of samples from the S3 bucket
    :param s3client: the s3client object to use to fetch
    :param samples_bucket: the name of the samples bucket
    :param samples_path: the path of the samples object
    :param member_id: the ID of the member to retrieve
    :return: a list of samples
    """

    key = f"{samples_path}member-{member_id}.jsonl"

    data = (
        s3client.get_object(Bucket=samples_bucket, Key=key)["Body"]
        .read()
        .decode("utf-8")
    )

    from io import StringIO
    import logging

    with StringIO(data) as json_file:
        output = list(json_file)
        logging.info(f"Found {len(output)} samples for " f"member {member_id}")
        return output


def preservation_status(result) -> (dict, str):
    """
    Return preservation statistics for a specific member
    :param result: the pre-parsed JSON entry of the member
    :return: 2-tuple: dictionary of preservations and the DOI string
    """
    from utils import show_preservation

    container_title = (
        result["container-title"] if "container-title" in result else None
    )
    issn = result["ISSN"] if "ISSN" in result else None
    volume = result["volume"] if "volume" in result else None

    # not in sampling framework (yet)
    no = None

    return show_preservation(
        container_title=container_title,
        issn=issn,
        volume=volume,
        no=no,
        doi=result,
    )


def process_member_sample(samples, sample_path, verbose=False) -> dict:
    """
    Processes samples for a single member
    :param samples: the samples to process
    :param sample_path: the path of the sample
    :param verbose: whether or not to print the sample
    :return: a dictionary of preservation statistics
    """
    from constants import archives
    from datetime import datetime
    import json

    from collections import defaultdict

    overall_status: DefaultDict[Any, Any] = defaultdict(int)

    # date stamp this output
    overall_status["about"] = {
        "date-generated": str(datetime.now()),
        "sample-file": sample_path,
    }

    three_archives = 0
    two_archives = 0
    one_archive = 0

    for sample_item in samples:
        result = json.loads(sample_item)["data-point"]

        overall_status["about"]["member"] = result["member"]

        # we can only work with journal articles
        # we exclude journal articles from the current year because they
        # most likely have not been ingested into digital preservation
        # systems yet
        if "type" in result and result["type"] == "journal-article":
            year_published = (
                result["published"]["date-parts"][0][0]
                if "published" in result
                else None
            )

            if year_published and year_published != date.today().year:
                has_preservation = False
                archive_count = 0

                preservation_statuses, doi = preservation_status(result)

                # increment the sample count
                overall_status["sample-count"] += 1

                for key, value in preservation_statuses.items():
                    preserved, done = value

                    if preserved:
                        has_preservation = True

                        # increment this archive's stats
                        overall_status[key] += 1

                        # increment the archive counter
                        archive_count += 1

                        # increment total preservation instances count
                        overall_status["preservation-instances"] += 1

                # preserved_count refers to the number of works with at
                # least one preservation
                if has_preservation:
                    overall_status["preserved-count"] += 1

                    if verbose:
                        logging.info(f"{doi['DOI']} has a preservation")
                        logging.info(
                            f"Running total: "
                            f"{overall_status['preserved-count']} preserved, "
                            f"{overall_status['unpreserved-count']} unpreserved"
                        )

                else:
                    overall_status["unpreserved-count"] += 1

                    if verbose:
                        logging.info(f"{doi['DOI']} has no preservation")
                        logging.info(
                            f"Running total: "
                            f"{overall_status['preserved-count']} preserved, "
                            f"{overall_status['unpreserved-count']} unpreserved"
                        )

                # increment the correct counters for overall stats
                if archive_count == 1:
                    one_archive += 1
                elif archive_count == 2:
                    two_archives += 1
                elif archive_count > 2:
                    three_archives += 1
        else:
            # this is an excluded sample item
            if "type" in result and result["type"] != "journal-article":
                overall_status["excluded-non-journal"] += 1
                if verbose:
                    logging.info(
                        f"{result['DOI']} is excluded as it is not a journal "
                        f"article"
                    )
            elif "published" not in result:
                overall_status["excluded-no-date"] += 1
                if verbose:
                    logging.info(
                        f"{result['DOI']} is excluded as it is not a journal "
                        f"article"
                    )
            elif date.today().year == result["published"]["date-parts"][0][0]:
                overall_status["excluded-current-year"] += 1
                if verbose:
                    logging.info(
                        f"{result['DOI']} is excluded as is too recent"
                    )

    # add blank keys for archives that weren't used
    for preservation_system, class_o in archives.items():
        if class_o.name() not in overall_status:
            overall_status[class_o.name()] = 0

    # calculate percentage of preservation
    if overall_status["sample-count"] > 0:
        overall_status["percentage-preserved"] = (
            overall_status["preserved-count"] / overall_status["sample-count"]
        ) * 100
    else:
        overall_status["percentage-preserved"] = 0

    # add the counters
    overall_status["preserved-in-one-archive"] = one_archive
    overall_status["preserved-in-two-archives"] = two_archives
    overall_status["preserved-in-three-or-more-archives"] = three_archives

    # determine the classes
    overall_status["member-grade"] = "Unclassified"

    if overall_status["sample-count"] > 0:
        # 25% in 1 archive
        if one_archive / overall_status["sample-count"] >= 0.25:
            overall_status["member-grade"] = "Bronze"

        # 50% in 2 archives
        if two_archives / overall_status["sample-count"] >= 0.50:
            overall_status["member-grade"] = "Silver"

        # 75% in 3 archives
        if three_archives / overall_status["sample-count"] >= 0.75:
            overall_status["member-grade"] = "Gold"

    return overall_status


def push_json_to_s3(
    s3,
    json_obj,
    member_id,
    annotation_bucket,
    annotation_path,
    annotation_filename,
) -> None:
    """
    Writes the JSON data to S3
    :param s3: the s3 object to use
    :param annotation_bucket: the name of the annotation bucket
    :param annotation_path: the path of the annotation object
    :param annotation_filename: the name of the annotation file
    :param json_obj: the JSON to write
    :param member_id: the member ID into which to write
    :return:
    """
    import json
    import logging

    logging.info("Writing JSON to S3")
    key = f"{annotation_path}/members/{member_id}/{annotation_filename}"

    obj = s3.Object(annotation_bucket, key)
    obj.put(Body=json.dumps(json_obj))


def process_sample(
    annotation_bucket,
    annotation_filename,
    annotation_path,
    samples_bucket,
    samples_path,
    member_id,
    code_bucket,
    verbose=False,
):
    """
    Process a single member sample
    :param annotation_bucket: the annotation bucket
    :param annotation_filename: the annotation filename
    :param annotation_path: the annotation path
    :param samples_bucket: the samples bucket
    :param samples_path: the samples path
    :param member_id: the member id
    :param verbose: whether or not to print status messages
    :param code_bucket: the code bucket where settings are located
    :return:
    """
    import logging

    import boto3

    s3client = boto3.client("s3")
    session = boto3.Session()
    s3 = session.resource("s3")

    import environment

    environment.setup_environment(code_bucket, download_settings=False)

    logging.info(f"Processing member {member_id}")

    samples = get_samples(
        s3client,
        member_id,
        samples_bucket=samples_bucket,
        samples_path=samples_path,
    )

    overall_status = process_member_sample(
        samples, samples_path, verbose=verbose
    )

    push_json_to_s3(
        s3,
        overall_status,
        member_id,
        annotation_bucket=annotation_bucket,
        annotation_path=annotation_path,
        annotation_filename=annotation_filename,
    )

    return {member_id: overall_status}


def generate_report():
    SAMPLES_BUCKET = "samples-crossref-research"
    SAMPLES_PATH = "members-works/sample-2023-01-21/works/"

    ANNOTATION_BUCKET = "outputs.research.crossref.org"
    ANNOTATION_PATH = "annotations"
    ANNOTATION_FILENAME = "preservation.json"

    CODE_BUCKET = "airflow-crossref-research-annotation"

    PARALLEL_JOBS = 5

    import boto3
    import logging

    s3client = boto3.client("s3")

    from joblib import Parallel, delayed

    # get member list from S3
    members = get_members(
        s3client=s3client,
        samples_bucket=SAMPLES_BUCKET,
        samples_path=SAMPLES_PATH,
    )

    logging.info(f"There are {len(members)} to process.")

    # the results of the parallel processing are dictionaries with
    # the member ID as the key and a dictionary of preservation statistics
    # as the value.

    results = Parallel(n_jobs=PARALLEL_JOBS)(
        delayed(process_sample)(
            ANNOTATION_BUCKET,
            ANNOTATION_FILENAME,
            ANNOTATION_PATH,
            SAMPLES_BUCKET,
            SAMPLES_PATH,
            member_id,
            CODE_BUCKET,
        )
        for member_id in members
    )

    return members


def overall_report(members):
    SAMPLES_BUCKET = "samples-crossref-research"
    SAMPLES_PATH = "members-works/sample-2023-01-21/works/"

    ANNOTATION_BUCKET = "outputs.research.crossref.org"
    ANNOTATION_PATH = "annotations"
    ANNOTATION_FILENAME = "preservation.json"

    CODE_BUCKET = "airflow-crossref-research-annotation"

    PARALLEL_JOBS = 5

    import boto3
    import logging

    s3client = boto3.client("s3")

    # overall reports we want to build:
    # 1. Breakdown by member size
    # 2. Totally unpreserved members ["percentage-preserved"]
    # 3. Members with 75% in three archives (gold standard) ["member-grade"]
    # 4. Members with 50% in two archives (silver standard) ["member-grade"]
    # 5. Members with 25% in one archive (bronze standard) ["member-grade"]

    member_tier_names = [
        "<USD 1 million",
        "USD 1 million - USD 5 million",
        "USD 5 million - USD 10 million",
        "USD 10 million - USD 25 million",
        "USD 25 million - USD 50 million",
        "USD 50 million - USD 100 million",
        "USD 100 million - USD 200 million",
        "USD 200 million - USD 500 million",
        ">USD 500 million",
    ]

    member_tiers = {
        "<USD 1 million": 275,
        "USD 1 million - USD 5 million": 550,
        "USD 5 million - USD 10 million": 1650,
        "USD 10 million - USD 25 million": 3900,
        "USD 25 million - USD 50 million": 8300,
        "USD 50 million - USD 100 million": 14000,
        "USD 100 million - USD 200 million": 22000,
        "USD 200 million - USD 500 million": 33000,
        ">USD 500 million": 50000,
    }

    gold_members = {member_tier: 0 for member_tier in member_tier_names}
    silver_members = {member_tier: 0 for member_tier in member_tier_names}
    bronze_members = {member_tier: 0 for member_tier in member_tier_names}
    unclassified_members = {member_tier: 0 for member_tier in member_tier_names}

    for member in members:
        preservations = get_annotation(
            s3client=s3client,
            annotations_bucket=ANNOTATION_BUCKET,
            annotations_path=ANNOTATION_PATH,
            member_id=member,
            annotation_name="preservation.json",
        )

        member_data = get_annotation(
            s3client=s3client,
            member_id=member,
            annotations_bucket=ANNOTATION_BUCKET,
            annotations_path=ANNOTATION_PATH,
            annotation_name="member-profile.json",
        )

        annual_fee = int(member_data["annual-fee"])
        member_band = None

        for key, val in member_tiers.items():
            if annual_fee <= val:
                # put this member in this band
                member_band = key

        if not member_band:
            logging.warning(f"Unable to classify this member ({member})")

        # this calculates the preservation grades for different member tiers
        # using fee level as the benchmark
        if preservations["member-grade"] == "Bronze":
            bronze_members[member_band] += 1
        elif preservations["member-grade"] == "Silver":
            silver_members[member_band] += 1
        elif preservations["member-grade"] == "Gold":
            gold_members[member_band] += 1
        else:
            unclassified_members[member_band] += 1

        pass

    gold_totals = sum(gold_members.values())
    silver_totals = sum(silver_members.values())
    bronze_totals = sum(bronze_members.values())
    unclassified_totals = sum(unclassified_members.values())

    return


def get_annotation(
    s3client, member_id, annotations_bucket, annotations_path, annotation_name
):
    key = f"{annotations_path}/members/{member_id}/{annotation_name}.jsonl"

    data = (
        s3client.get_object(Bucket=annotations_bucket, Key=key)["Body"]
        .read()
        .decode("utf-8")
    )

    from io import StringIO
    import logging
    import json

    with StringIO(data) as json_file:
        output = json.loads(json_file.read())
        return output
