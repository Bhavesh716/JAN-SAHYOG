# JAN SAHYOG — Data Sources & Knowledge Policy

## 1. Purpose

JAN SAHYOG depends on trustworthy and up-to-date information. This document describes the intended source categories and the checks required before documents are indexed.

## 2. Intended Source Categories

Prioritize official publishers and source material relevant to the user's question.

| Topic | Preferred source category | Example material |
|---|---|---|
| Cooperative laws and by-laws | Relevant government department / official gazette | Acts, rules, model by-laws, amendments |
| Ministry of Cooperation schemes | Ministry of Cooperation | Scheme pages, guidelines, circulars, FAQs |
| PACS services | Ministry / relevant cooperative authorities | PACS guidance, scheme details, service procedures |
| PMFBY | Official PMFBY portal and responsible government departments | Operational guidelines, notifications, FAQs |
| Agricultural support | Relevant central/state government departments | Scheme guidance and official advisories |
| Financial literacy | RBI and other relevant official financial authorities | Consumer education, banking safety, financial awareness |
| Grievance redressal | Responsible department or authorized grievance portal | Filing procedures, escalation steps, official contact details |

These are source categories, not a claim that every source has been connected or every dataset has been collected.

## 3. Source Registry

For each document, maintain metadata such as:

- Document title
- Publisher / issuing authority
- Canonical source URL
- Document type
- Publication date
- Last updated date, if available
- Applicable state, language, or scheme
- Version or notification number
- Date retrieved
- Review status
- SHA-256 checksum
- Superseded / active status, where known

The starter ingestion script records basic file metadata. Extend it to include this source registry before using the knowledge base for real public guidance.

## 4. Review Before Indexing

Before a document is treated as an approved source:

1. Confirm that the publisher is appropriate for the topic.
2. Check that the URL or document is authentic.
3. Record its date and applicability.
4. Check whether a newer circular or version replaces it.
5. Confirm permission and usage conditions.
6. Mark the document as reviewed by an authorized reviewer.

A file being present in the repository does not mean its contents are verified or current.

## 5. Updates and Retention

- Recheck frequently changing scheme information on a defined schedule.
- Preserve version metadata for auditability.
- Remove or mark superseded chunks when documents change.
- Record ingestion time and source checksum.
- Keep a process for correcting errors.
- Do not silently treat old documents as current.

## 6. User-Facing Citations

Where possible, show the source title, issuing authority, date/version, and a link to the official page. If the system cannot find relevant reviewed information, it should state that it could not verify the answer.

## 7. Personal and Sensitive Data

Do not include real user documents, Aadhaar details, bank details, phone numbers, or other sensitive personal data in the public repository or sample knowledge base. Use synthetic examples for development and testing.
