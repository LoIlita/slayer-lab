"""EMAIL_PROSE_OBF (mat_wybor.premask_emails(prose_obf=True)): addresses seen in the 2026-11-27 scan of the web sources are
masked whole, prose and maths that look alike are left alone. Addresses below are invented (same shapes as the real ones)."""
import sys

import pytest

sys.modules.setdefault("pii", type(sys)("pii"))
import mat_wybor  # noqa: E402


def mask(t: str) -> str:
    return mat_wybor._mask_emails(t, prose_obf=True)[0]


@pytest.mark.parametrize("before, after", [
    ("From: Jan Kowal <jkowal_at_uni.edu>\nDate: Tue", "From: Jan Kowal <[PII]>\nDate: Tue"),
    ("send me an e-mail at R_dot_Kow_at_ieee_dot_org.", "send me an e-mail at [PII]."),
    ("Md. Jan Kowal jkowal_at_uni.ac.bd\n2", "Md. Jan Kowal [PII]\n2"),
    ("(jkowal{at}hosp.nhs.uk)", "([PII])"),
    ("Kowal <jan.kowal <at> uni.edu> writes:", "Kowal <[PII]> writes:"),
    ("jkowal <at>yahoo<dot>com", "[PII]"),
    ("questions (tom<AT>eit.lth.se).", "questions ([PII])."),
    ("email me at jkowal at gmail dot com with", "email me at [PII] with"),
    ("e-mail: first dot last at gmail dot com)", "e-mail: [PII])"),
    ("E-mail: kowal at math dot uga dot edu Office", "E-mail: [PII] Office"),
    ("attachment to jkowal AT holy.edu.", "attachment to [PII]."),
    ("Jan Kowal jan.kowal at univ-brest.fr\nMon Jul 1 12:29:23 CEST 2002",
     "Jan Kowal [PII]\nMon Jul 1 12:29:23 CEST 2002"),
    ("Jan Kowal jkowal at u.washington.edu\nTue Jul 18 16:55:31 CEST 2006",
     "Jan Kowal [PII]\nTue Jul 18 16:55:31 CEST 2006"),
    ("jk at crypt.org jk at crypt.org\nSun Jul 17 10:31:46 CEST 2011", "[PII] [PII]\nSun Jul 17 10:31:46 CEST 2011"),
    ("On Sun, Mrs Kowal <kowal at uic.edu> wrote:", "On Sun, Mrs Kowal <[PII]> wrote:"),
    ("Kantor (jkan at nd.edu); the content", "Kantor ([PII]); the content"),
    ("Is n.s.kowal_at_nl.ibm.com Ok with you?", "Is [PII] Ok with you?"),
    ("Cambridge, Email:jkowal at cmgm.stanford.edu\nCambridge", "Cambridge, Email:[PII]\nCambridge"),
    ("<mailto:jk at centertap.com.br>jk", "<mailto:[PII]>jk"),
    ("> To: jkowal at WPI.EDU\n> Subject:", "> To: [PII]\n> Subject:"),
    ("my e-mail is jkowal.x{at}yahoo{dot}com. We", "my e-mail is [PII]. We"),
    ("From: Jan Kowal <kowal%home.csc.ti.com at RELAY.CS.NET>\n", "From: Jan Kowal <[PII]>\n"),
    ("From: Jan Kowal [jkowal at UGA.EDU]\nSent:", "From: Jan Kowal [[PII]]\nSent:"),
    ("Jan A. Kowal jkowal at Filker.Org\nSun, 1 Dec 2002 00:54:46 -0500", "Jan A. Kowal [PII]\nSun, 1 Dec 2002 00:54:46 -0500"),
    ("Jan Kowal\njkowal at uni.co.uk\nhttp://www.uni.co.uk/~jk", "Jan Kowal\n[PII]\nhttp://www.uni.co.uk/~jk"),
    ("> Jan Kowal jk at kowal.org.uk\n> Wed Sep 29 13:39:10 BST 2004", "> Jan Kowal [PII]\n> Wed Sep 29 13:39:10 BST 2004"),
    ("jk at netcom.com          herein are mine", "[PII]          herein are mine"),
    ("Prof : Jan KOWAL   jkowal at skku.edu\n", "Prof : Jan KOWAL   [PII]\n"),
    ("rhk at mindspring.com\nrhk at att.net (either)", "[PII]\n[PII] (either)"),
    ("In a message dated 2001/1/9, jkowal at uni.edu writes:", "In a message dated 2001/1/9, [PII] writes:"),
    ("In article <x>, withk at wolfram.com (Jan\nKowal) wrote:", "In article <x>, [PII] (Jan\nKowal) wrote:"),
    ("on 8/4/00 7:19 AM, Jan Kowal at jk at earthlink.net wrote:", "on 8/4/00 7:19 AM, Jan Kowal at [PII] wrote:"),
    ("Rog <rog at pynguins.com <mailto:", "Rog <[PII] <mailto:"),
    ("or via e-mail to wrtc at maspar.com.", "or via e-mail to [PII]."),
    ("• Reply-to: hanl at cox.net\n", "• Reply-to: [PII]\n"),
    ("Prof : Jan KOWAL \xa0\xa0jk at skku.edu\n", "Prof : Jan KOWAL \xa0\xa0[PII]\n"),
    ("Karanth <shk at amba.com\n> > wrote:", "Karanth <[PII]\n> > wrote:"),
    ("<mailto:x>ck at centertap.com.br<mailto:y>", "<mailto:x>[PII]<mailto:y>"),
])
def test_masked(before, after):
    assert mask(before) == after


@pytest.mark.parametrize("text", [
    "we arrive at a dot in the $3$ column",
    "looks at the dot in front of him",
    "the electric field at the dot in the figure",
    "she looks carefully at each dot in turn",
    "YOU CAN ALWAYS FIND ME AT dansmath.com - Dan",
    "e.g. at amazon.com you can buy it",
    "The book is available at Amazon.com (available at amazon.com) and [Available at Amazon.com].",
    "Worksheet\nCreated at edHelper.Com\n",
    "Thanks!\nCrossposted at Math.SE\n",
    "the answer here (and at math.SE) helped, ask here (or at money.SE)",
    "I have an account at gmail.com for that",
    "Note: the book is at amazon.com; From: here to there",
    "the source is at github.com/user/repo and index.html at www.site.org/x",
    "f at x equals 2, g at y.z, evaluate obj_at_index and value_at_risk",
    "write to jkowal@example.com",  # '@' addresses: EMAIL, not this rule; example domain stays
    "x_at_example.com",
    "Posted at 10:22 Mon Jul 1 12:29:23 2002",
])
def test_left_alone(text):
    expected = mat_wybor._mask_emails(text)[0]  # only the rules that were on before
    assert mask(text) == expected
