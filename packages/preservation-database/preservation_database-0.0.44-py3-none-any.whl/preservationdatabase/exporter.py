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
    doi = result["DOI"]

    # not in sampling framework (yet)
    no = None

    return show_preservation(container_title, issn, volume, no, doi)


def process_member_sample(samples, sample_path) -> dict:
    """
    Processes samples for a single member
    :param samples: the samples to process
    :param sample_path: the path of the sample
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

    for sample_item in samples:
        result = json.loads(sample_item)["data-point"]

        # we can only work with journal articles
        if "type" in result and result["type"] == "journal-article":
            preservation_statuses, doi = preservation_status(result)
            has_preservation = False

            # increment the sample count
            overall_status["sample-count"] += 1

            for key, value in preservation_statuses.items():
                preserved, done = value

                if preserved:
                    has_preservation = True

                    # increment this archive's stats
                    overall_status[key] += 1

                    # increment total preservation instances count
                    overall_status["preservation-instances"] += 1

            # preserved_count refers to the number of items with at
            # least one preservation
            if has_preservation:
                overall_status["preserved_count"] += 1

    # add blank keys for archives that weren't used
    for preservation_system, class_o in archives.items():
        if class_o.name() not in overall_status:
            overall_status[class_o.name()] = 0

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
):
    """
    Process a single member sample
    :param annotation_bucket: the annotation bucket
    :param annotation_filename: the annotation filename
    :param annotation_path: the annotation path
    :param samples_bucket: the samples bucket
    :param samples_path: the samples path
    :param member_id: the member id
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

    overall_status = process_member_sample(samples, samples_path)

    push_json_to_s3(
        s3,
        overall_status,
        member_id,
        annotation_bucket=annotation_bucket,
        annotation_path=annotation_path,
        annotation_filename=annotation_filename,
    )
