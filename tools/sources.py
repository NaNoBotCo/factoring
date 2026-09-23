# -*- coding: utf-8 -*-
"""sources.py — every source the site cites, numbered once.

cite_html(ids) renders a bracketed run of numbers linking to /sources/#id. Data rows
(timeline, records, claims, estimates, ledger) name sources by these ids and the build
refuses an id that is not here.
"""
from __future__ import annotations

SOURCES = {
    # ---------------------------------------------------------------- the old ideas
    "nicomachus": ("Nicomachus of Gerasa", "Introduction to Arithmetic, book I ch. 13 — the earliest written description of the sieve, credited to Eratosthenes", "c. 100 AD; English by M. L. D'Ooge, 1926", "https://archive.org/details/NicomachusIntroToArithmetic"),
    "fermat1643": ("Pierre de Fermat", "Letter to Marin Mersenne on a method of factoring, with 2027651281 = 44021 × 46061 as the example", "1643; in Dickson, History of the Theory of Numbers vol. I ch. XIV", "https://archive.org/details/historyoftheoryo01dick"),
    "euler1732": ("Leonhard Euler", "Observationes de theoremate quodam Fermatiano aliisque ad numeros primos spectantibus (E26) — 2^32 + 1 = 641 × 6700417", "Commentarii academiae scientiarum Petropolitanae 6, 1738 (presented 1732)", "https://scholarlycommons.pacific.edu/euler-works/26/"),
    "gauss1801": ("Carl Friedrich Gauss", "Disquisitiones Arithmeticae, art. 329 — on the problem of telling primes from composites and splitting the latter", "Leipzig, 1801; English by A. A. Clarke, 1966", "https://archive.org/details/disquisitionesar00gaus"),
    "riemann1859": ("Bernhard Riemann", "Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse", "Monatsberichte der Berliner Akademie, November 1859", "https://www.claymath.org/collections/riemanns-1859-manuscript/"),
    "hadamard1896": ("Jacques Hadamard", "Sur la distribution des zéros de la fonction ζ(s) et ses conséquences arithmétiques", "Bulletin de la Société Mathématique de France 24 (1896) 199–220", "https://doi.org/10.24033/bsmf.545"),
    "hilbert1900": ("David Hilbert", "Mathematische Probleme — the eighth problem", "Göttinger Nachrichten, 1900; English in Bull. AMS 8 (1902) 437–479", "https://www.ams.org/journals/bull/1902-08-10/S0002-9904-1902-00923-3/"),
    "lehmer1933": ("D. H. Lehmer", "A photo-electric number sieve", "American Mathematical Monthly 40 (1933) 401–406", "https://doi.org/10.2307/2301846"),
    "kraitchik1926": ("Maurice Kraitchik", "Théorie des nombres, tome II — the idea of combining congruences into a square", "Gauthier-Villars, Paris, 1926", "https://gallica.bnf.fr/ark:/12148/bpt6k9642636x"),
    "turing1953": ("Alan Turing", "Some calculations of the Riemann zeta-function — zeros checked on the Manchester machine in 1950", "Proceedings of the London Mathematical Society s3-3 (1953) 99–117", "https://doi.org/10.1112/plms/s3-3.1.99"),
    # ---------------------------------------------------------------- the modern methods
    "morrison1975": ("Michael A. Morrison and John Brillhart", "A method of factoring and the factorization of F7", "Mathematics of Computation 29 (1975) 183–205", "https://doi.org/10.1090/S0025-5718-1975-0371800-5"),
    "pollard1974": ("J. M. Pollard", "Theorems on factorization and primality testing — the p − 1 method", "Mathematical Proceedings of the Cambridge Philosophical Society 76 (1974) 521–528", "https://doi.org/10.1017/S0305004100049252"),
    "pollard1975": ("J. M. Pollard", "A Monte Carlo method for factorization — the rho method", "BIT Numerical Mathematics 15 (1975) 331–334", "https://doi.org/10.1007/BF01933667"),
    "miller1976": ("Gary L. Miller", "Riemann's hypothesis and tests for primality", "Journal of Computer and System Sciences 13 (1976) 300–317", "https://doi.org/10.1016/S0022-0000(76)80043-8"),
    "rsa1978": ("R. L. Rivest, A. Shamir and L. Adleman", "A method for obtaining digital signatures and public-key cryptosystems", "Communications of the ACM 21 (1978) 120–126", "https://doi.org/10.1145/359340.359342"),
    "gardner1977": ("Martin Gardner", "A new kind of cipher that would take millions of years to break — the RSA-129 challenge", "Scientific American 237, August 1977, 120–124", "https://www.scientificamerican.com/article/mathematical-games-1977-08/"),
    "dixon1981": ("John D. Dixon", "Asymptotically fast factorization of integers", "Mathematics of Computation 36 (1981) 255–260", "https://doi.org/10.1090/S0025-5718-1981-0595059-1"),
    "pomerance1985": ("Carl Pomerance", "The quadratic sieve factoring algorithm", "Advances in Cryptology, EUROCRYPT '84, LNCS 209 (1985) 169–182", "https://doi.org/10.1007/3-540-39757-4_17"),
    "pomerance1996": ("Carl Pomerance", "A tale of two sieves", "Notices of the American Mathematical Society 43 (1996) 1473–1485", "https://www.ams.org/notices/199612/pomerance.pdf"),
    "lenstra1987": ("H. W. Lenstra Jr.", "Factoring integers with elliptic curves", "Annals of Mathematics 126 (1987) 649–673", "https://doi.org/10.2307/1971363"),
    "lenstra1993": ("A. K. Lenstra, H. W. Lenstra Jr., M. S. Manasse and J. M. Pollard", "The factorization of the ninth Fermat number", "Mathematics of Computation 61 (1993) 319–349", "https://doi.org/10.1090/S0025-5718-1993-1182953-4"),
    "nfs1993": ("A. K. Lenstra and H. W. Lenstra Jr. (eds.)", "The development of the number field sieve", "Lecture Notes in Mathematics 1554, Springer, 1993", "https://doi.org/10.1007/BFb0091534"),
    "atkins1995": ("Derek Atkins, Michael Graff, Arjen K. Lenstra and Paul C. Leyland", "The magic words are squeamish ossifrage — RSA-129", "Advances in Cryptology, ASIACRYPT '94, LNCS 917 (1995) 261–277", "https://doi.org/10.1007/BFb0000440"),
    "cavallar2000": ("Stefania Cavallar and 16 others", "Factorization of a 512-bit RSA modulus", "Advances in Cryptology, EUROCRYPT 2000, LNCS 1807, 1–18", "https://doi.org/10.1007/3-540-45539-6_1"),
    "kleinjung2010": ("Thorsten Kleinjung and 12 others", "Factorization of a 768-bit RSA modulus", "Advances in Cryptology, CRYPTO 2010, LNCS 6223, 333–350; IACR ePrint 2010/006", "https://eprint.iacr.org/2010/006"),
    "boudot2020": ("Fabrice Boudot, Pierrick Gaudry, Aurore Guillevic, Nadia Heninger, Emmanuel Thomé and Paul Zimmermann", "Comparing the difficulty of factorization and discrete logarithm: a 240-digit experiment", "Advances in Cryptology, CRYPTO 2020; IACR ePrint 2020/697", "https://eprint.iacr.org/2020/697"),
    "rsa250": ("Paul Zimmermann", "Factorization of RSA-250 — announcement to the cado-nfs list", "28 February 2020", "https://sympa.inria.fr/sympa/arc/cado-nfs/2020-02/msg00001.html"),
    "cadonfs": ("The CADO-NFS development team", "CADO-NFS, an implementation of the number field sieve", "INRIA, release 2.3.0 and later", "https://cado-nfs.inria.fr/"),
    "rsanumbers": ("Wikipedia contributors", "RSA numbers — the challenge list with each factorization's date, team and effort", "Wikipedia, read September 2026", "https://en.wikipedia.org/wiki/RSA_numbers"),
    "cunningham": ("Samuel Wagstaff Jr. (ed.)", "The Cunningham Project — factorizations of b^n ± 1, kept since 1925", "Purdue University", "https://homes.cerias.purdue.edu/~ssw/cun/"),
    "adrian2015": ("David Adrian and 13 others", "Imperfect forward secrecy: how Diffie-Hellman fails in practice — the Logjam attack and 512-bit keys", "ACM CCS 2015", "https://weakdh.org/imperfect-forward-secrecy-ccs15.pdf"),
    "valenta2015": ("Luke Valenta, Shaanan Cohney, Alex Liao, Joshua Fried, Satya Bodduluri and Nadia Heninger", "Factoring as a service — a 512-bit RSA key in four hours for $75 of cloud time", "Financial Cryptography 2016; IACR ePrint 2015/1000", "https://eprint.iacr.org/2015/1000"),
    "aks2004": ("Manindra Agrawal, Neeraj Kayal and Nitin Saxena", "PRIMES is in P", "Annals of Mathematics 160 (2004) 781–793", "https://doi.org/10.4007/annals.2004.160.781"),
    # ---------------------------------------------------------------- Riemann
    "montgomery1973": ("Hugh L. Montgomery", "The pair correlation of zeros of the zeta function", "Analytic Number Theory, Proc. Sympos. Pure Math. 24 (1973) 181–193", "https://doi.org/10.1090/pspum/024"),
    "odlyzko1987": ("Andrew M. Odlyzko", "On the distribution of spacings between zeros of the zeta function", "Mathematics of Computation 48 (1987) 273–308", "https://doi.org/10.1090/S0025-5718-1987-0866115-0"),
    "odlyzkotables": ("Andrew M. Odlyzko", "Tables of zeros of the Riemann zeta function", "University of Minnesota", "https://www-users.cse.umn.edu/~odlyzko/zeta_tables/"),
    "berry1999": ("Michael V. Berry and Jonathan P. Keating", "The Riemann zeros and eigenvalue asymptotics", "SIAM Review 41 (1999) 236–266", "https://doi.org/10.1137/S0036144598347497"),
    "clay": ("Clay Mathematics Institute", "The Riemann Hypothesis — Millennium Prize problem statement by Enrico Bombieri", "2000", "https://www.claymath.org/millennium/riemann-hypothesis/"),
    "guth2024": ("Larry Guth and James Maynard", "New large value estimates for Dirichlet polynomials", "arXiv:2405.20552, May 2024", "https://arxiv.org/abs/2405.20552"),
    "zhang2022": ("Yitang Zhang", "Discrete mean estimates and the Landau-Siegel zero", "arXiv:2211.02515, November 2022", "https://arxiv.org/abs/2211.02515"),
    "platt2021": ("Dave Platt and Tim Trudgian", "The Riemann hypothesis is true up to 3·10^12", "Bulletin of the London Mathematical Society 53 (2021) 792–797", "https://doi.org/10.1112/blms.12460"),
    # ---------------------------------------------------------------- quantum
    "shor1997": ("Peter W. Shor", "Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer", "SIAM Journal on Computing 26 (1997) 1484–1509; first given at FOCS 1994", "https://arxiv.org/abs/quant-ph/9508027"),
    "vandersypen2001": ("Lieven M. K. Vandersypen, Matthias Steffen, Gregory Breyta, Costantino S. Yannoni, Mark H. Sherwood and Isaac L. Chuang", "Experimental realization of Shor's quantum factoring algorithm using nuclear magnetic resonance — 15 = 3 × 5", "Nature 414 (2001) 883–887", "https://doi.org/10.1038/414883a"),
    "martinlopez2012": ("Enrique Martín-López, Anthony Laing, Thomas Lawson, Roberto Alvarez, Xiao-Qi Zhou and Jeremy L. O'Brien", "Experimental realization of Shor's quantum factoring algorithm using qubit recycling — 21 = 3 × 7", "Nature Photonics 6 (2012) 773–776", "https://arxiv.org/abs/1111.4147"),
    "xu2012": ("Nanyang Xu, Jing Zhu, Dawei Lu, Xianyi Zhou, Xinhua Peng and Jiangfeng Du", "Quantum factorization of 143 on a dipolar-coupling nuclear magnetic resonance system", "Physical Review Letters 108, 130501 (2012)", "https://doi.org/10.1103/PhysRevLett.108.130501"),
    "dattani2014": ("Nikesh S. Dattani and Nathaniel Bryans", "Quantum factorization of 56153 with only 4 qubits", "arXiv:1411.6758, 2014", "https://arxiv.org/abs/1411.6758"),
    "smolin2013": ("John A. Smolin, Graeme Smith and Alexander Vargo", "Oversimplifying quantum factoring", "Nature 499 (2013) 163–165", "https://arxiv.org/abs/1301.7007"),
    "monz2016": ("Thomas Monz and 8 others", "Realization of a scalable Shor algorithm — 15 on five trapped ions", "Science 351 (2016) 1068–1070", "https://arxiv.org/abs/1507.08852"),
    "amico2019": ("Mirko Amico, Zain H. Saleem and Muir Kumph", "An experimental study of Shor's factoring algorithm on IBM Q — 35 attempted, noise wins", "Physical Review A 100, 012305 (2019)", "https://arxiv.org/abs/1903.00768"),
    "fowler2012": ("Austin G. Fowler, Matteo Mariantoni, John M. Martinis and Andrew N. Cleland", "Surface codes: towards practical large-scale quantum computation", "Physical Review A 86, 032324 (2012)", "https://arxiv.org/abs/1208.0928"),
    "gidney2019": ("Craig Gidney and Martin Ekerå", "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits", "Quantum 5, 433 (2021); arXiv May 2019", "https://arxiv.org/abs/1905.09749"),
    "gouzien2021": ("Élie Gouzien and Nicolas Sangouard", "Factoring 2048-bit RSA integers in 177 days with 13 436 qubits and a multimode memory", "Physical Review Letters 127, 140503 (2021)", "https://arxiv.org/abs/2103.06159"),
    "schnorr2021": ("Claus Peter Schnorr", "Fast factoring integers by SVP algorithms", "IACR ePrint 2021/232", "https://eprint.iacr.org/2021/232"),
    "yan2022": ("Bao Yan and 23 others", "Factoring integers with sublinear resources on a superconducting quantum processor — the 372-qubit claim", "arXiv:2212.12372, December 2022", "https://arxiv.org/abs/2212.12372"),
    "aaronson2023": ("Scott Aaronson", "Cargo cult quantum factoring", "Shtetl-Optimized, 4 January 2023", "https://scottaaronson.blog/?p=6957"),
    "regev2023": ("Oded Regev", "An efficient quantum factoring algorithm", "arXiv:2308.06572, August 2023; Journal of the ACM 72 (2025)", "https://arxiv.org/abs/2308.06572"),
    "ragavan2024": ("Seyoon Ragavan and Vinod Vaikuntanathan", "Space-efficient and noise-robust quantum factoring", "Advances in Cryptology, CRYPTO 2024; arXiv:2310.00899", "https://arxiv.org/abs/2310.00899"),
    "gidney2025": ("Craig Gidney", "How to factor 2048 bit RSA integers with less than a million noisy qubits", "arXiv:2505.15917, May 2025", "https://arxiv.org/abs/2505.15917"),
    "roetteler2017": ("Martin Roetteler, Michael Naehrig, Krysta M. Svore and Kristin Lauter", "Quantum resource estimates for computing elliptic curve discrete logarithms", "Advances in Cryptology, ASIACRYPT 2017; arXiv:1706.06752", "https://arxiv.org/abs/1706.06752"),
    "webber2022": ("Mark Webber, Vincent Elfving, Sebastian Weidt and Winfried K. Hensinger", "The impact of hardware specifications on reaching quantum advantage in the fault tolerant regime — breaking a Bitcoin key in 10 minutes, an hour, a day", "AVS Quantum Science 4, 013801 (2022)", "https://arxiv.org/abs/2108.12371"),
    "litinski2023": ("Daniel Litinski", "How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates", "arXiv:2306.08585, June 2023", "https://arxiv.org/abs/2306.08585"),
    "willow2024": ("Google Quantum AI", "Quantum error correction below the surface code threshold — the Willow chip", "Nature 638 (2025) 920–926; announced 9 December 2024", "https://www.nature.com/articles/s41586-024-08449-y"),
    "nist2024": ("National Institute of Standards and Technology", "NIST releases first three finalized post-quantum encryption standards — FIPS 203, 204, 205", "13 August 2024", "https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards"),
    "nist8547": ("National Institute of Standards and Technology", "Transition to post-quantum cryptography standards — NIST IR 8547 (initial public draft): RSA and ECC deprecated after 2030, disallowed after 2035", "November 2024", "https://csrc.nist.gov/pubs/ir/8547/ipd"),
    "gri2024": ("Michele Mosca and Marco Piani", "Quantum threat timeline report 2024 — the expert survey", "Global Risk Institute, December 2024", "https://globalriskinstitute.org/publication/2024-quantum-threat-timeline-report/"),
    # ---------------------------------------------------------------- the wallet
    "nakamoto2008": ("Satoshi Nakamoto", "Bitcoin: a peer-to-peer electronic cash system", "31 October 2008", "https://bitcoin.org/bitcoin.pdf"),
    "koblitz1987": ("Neal Koblitz", "Elliptic curve cryptosystems", "Mathematics of Computation 48 (1987) 203–209", "https://doi.org/10.1090/S0025-5718-1987-0866109-5"),
    "sec2": ("Certicom Research", "SEC 2: recommended elliptic curve domain parameters — secp256k1", "Standards for Efficient Cryptography, version 2.0, 2010", "https://www.secg.org/sec2-v2.pdf"),
    "btcdev": ("Bitcoin Project", "Developer guide — transactions, P2PKH, P2PK, P2WPKH and P2TR output types", "developer.bitcoin.org", "https://developer.bitcoin.org/devguide/transactions.html"),
    "bip340": ("Pieter Wuille, Jonas Nick and Tim Ruffing", "BIP 340 — Schnorr signatures for secp256k1", "2020", "https://github.com/bitcoin/bips/blob/master/bip-0340.mediawiki"),
    "bip341": ("Pieter Wuille, Jonas Nick and Anthony Towns", "BIP 341 — Taproot: SegWit version 1 spending rules (the output carries a public key)", "2020", "https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki"),
    "bip360": ("Hunter Beast and others", "BIP 360 — a quantum-resistant output type for Bitcoin", "bitcoin/bips, 2024 onward", "https://github.com/bitcoin/bips/blob/master/bip-0360.mediawiki"),
    "deloitte": ("Itan Barmes and Bram Bosch", "Quantum computers and the Bitcoin blockchain — the share of coins in exposed-key outputs", "Deloitte Netherlands", "https://www.deloitte.com/nl/en/services/risk-advisory/perspectives/quantum-computers-and-the-bitcoin-blockchain.html"),
    "lopp2025": ("Jameson Lopp, Christian Papathanasiou, Ludovic Perret, Kevin Le Bao and Trevor Ross", "Post quantum migration and legacy signature sunset — a BIP draft", "bitcoin-dev, July 2025", "https://github.com/jlopp/bips/blob/quantum_migration/bip-post-quantum-migration.mediawiki"),
    "bitcoinoptech": ("Bitcoin Optech", "Topic: quantum resistance", "bitcoinops.org", "https://bitcoinops.org/en/topics/quantum-resistance/"),
    # ---------------------------------------------------------------- 2024–2026, researched September 2026
    "chevignard2024": ("Clémence Chevignard, Pierre-Alain Fouque and André Schrottenloher", "Reducing the number of qubits in quantum factoring — RSA-2048 with about 1730 logical qubits", "Advances in Cryptology, CRYPTO 2025; IACR ePrint 2024/222", "https://eprint.iacr.org/2024/222"),
    "wang2024": ("Wang Chao and others (Shanghai University), reported by The Register", "A 22-bit RSA integer factored on a D-Wave annealer — the 'China breaks RSA' story", "Chinese Journal of Computers, 2024; The Register, 14 October 2024", "https://www.theregister.com/2024/10/14/china_quantum_attack/"),
    "wang2024b": ("Wang Chao and others (Shanghai University)", "A first successful factorization of RSA-2048 integer by D-Wave quantum computer — on integers whose two primes differ in two low bits", "Tsinghua Science and Technology, online 30 December 2024", "https://www.sciopen.com/article/10.26599/TST.2024.9010028"),
    "logical2024": ("Microsoft and Quantinuum", "Twelve logical qubits on the 56-qubit H2 trapped-ion machine", "Microsoft Azure Quantum blog, 10 September 2024", "https://azure.microsoft.com/en-us/blog/quantum/2024/09/10/microsoft-and-quantinuum-create-12-logical-qubits-and-demonstrate-a-hybrid-end-to-end-chemistry-simulation/"),
    "majorana2025": ("Adrian Cho, Science", "Debate erupts around Microsoft's blockbuster quantum computing claims — Majorana 1", "Science, 21 February 2025", "https://www.science.org/content/article/debate-erupts-around-microsoft-s-blockbuster-quantum-computing-claims"),
    "hqc2025": ("HPCwire", "NIST selects HQC as fifth algorithm for post-quantum encryption", "12 March 2025", "https://www.hpcwire.com/2025/03/12/nist-selects-hqc-as-fifth-algorithm-for-post-quantum-encryption/"),
    "wang2025": ("South China Morning Post", "China cracks another quantum code barrier — a 90-bit RSA integer on a D-Wave machine, reported without a paper", "April 2025", "https://www.scmp.com/news/china/science/article/3307487/china-cracks-another-quantum-code-barrier-how-much-longer-our-data-safe"),
    "qday2025": ("CoinDesk", "Quantum computing group offers 1 BTC to whoever breaks Bitcoin's cryptographic key — the Q-Day Prize opens", "17 April 2025", "https://www.coindesk.com/tech/2025/04/17/quantum-computing-group-offers-1-btc-to-whoever-breaks-bitcoin-s-cryptographic-key"),
    "ibm2025": ("IBM", "IBM sets the course to build the world's first large-scale, fault-tolerant quantum computer — Starling, 200 logical qubits by 2029", "IBM Quantum blog, 10 June 2025", "https://www.ibm.com/quantum/blog/large-scale-ftqc"),
    "tippeconnic2025": ("Steve Tippeconnic", "Quantum attack on a 5-bit elliptic curve key on IBM's 133-qubit ibm_torino", "arXiv:2507.10592, July 2025", "https://arxiv.org/abs/2507.10592"),
    "helios2025": ("Quantinuum", "Commercial launch of Helios — 98 trapped-ion qubits, 48 error-corrected logical qubits", "5 November 2025", "https://www.quantinuum.com/press-releases/quantinuum-announces-commercial-launch-of-new-helios-quantum-computer-that-offers-unprecedented-accuracy-to-enable-generative-quantum-ai-genqai"),
    "nighthawk2025": ("The Next Platform", "IBM lets fly Nighthawk and Loon QPUs on the way to quantum advantage", "12 November 2025", "https://www.nextplatform.com/compute/2025/11/12/ibm-lets-fly-nighthawk-and-loon-qpus-on-the-way-to-quantum-advantage/1689519"),
    "pinnacle2026": ("Mark Webster, Lucas Berent, Sunil Chandra, Ewan Hockings, Nouédyn Baspin, Frederik Thomsen, Alexander Smith and Oscar Cohen (Iceberg Quantum)", "The Pinnacle architecture — RSA-2048 with fewer than 100,000 physical qubits on qLDPC codes", "arXiv:2602.11457, February 2026", "https://arxiv.org/abs/2602.11457"),
    "aaronson2026": ("Scott Aaronson", "On the Pinnacle claim — serious work, engineering caveats, timeline effect unknown", "Shtetl-Optimized, 15 February 2026", "https://scottaaronson.blog/?p=9564"),
    "google2029": ("Heather Adkins and Sophie Schmieg, Google", "Google's post-quantum migration timeline — done by 2029", "Google blog, 25 March 2026", "https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/"),
    "babbush2026": ("Ryan Babbush, Lev Zalcman, Craig Gidney, Michael Broughton, Tanuj Khattar, Hartmut Neven, Thiago Bergamaschi, Justin Drake and Dan Boneh", "Resource estimates for breaking 256-bit elliptic curve keys — under 1,450 logical qubits, fewer than 500,000 physical, minutes of runtime", "arXiv:2603.28846, 30 March 2026", "https://arxiv.org/abs/2603.28846"),
    "googleblog2026": ("Ryan Babbush and Hartmut Neven", "Safeguarding cryptocurrency by disclosing quantum vulnerabilities responsibly", "Google Research blog, 31 March 2026", "https://research.google/blog/safeguarding-cryptocurrency-by-disclosing-quantum-vulnerabilities-responsibly/"),
    "caltech2026": ("Caltech and Oratomic", "Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits", "Caltech news, 31 March 2026", "https://www.caltech.edu/about/news/caltech-team-finds-useful-quantum-computers-could-be-built-with-as-few-as-10000-qubits"),
    "mundada2026": ("Pranav Mundada and others (Q-CTRL)", "A heterogeneous architecture for RSA-2048 in 9.2 days on 381,000 physical qubits", "arXiv:2604.06319, April 2026", "https://arxiv.org/abs/2604.06319"),
    "qday2026": ("Project Eleven", "The Q-Day Prize awarded for a 15-bit elliptic curve key recovered on IBM Heron processors", "24 April 2026", "https://www.projecteleven.com/blog/project-eleven-awards-1-btc-q-day-prize-for-largest-quantum-attack-on-elliptic-curve-cryptography-to-date"),
    "qday2026b": ("Bitcoin.com News", "IBM quantum hardware cracks 15-bit ECC key, but Bitcoin devs say random bits match the result", "24 April 2026", "https://news.bitcoin.com/ibm-quantum-hardware-cracks-15-bit-ecc-key-but-bitcoin-devs-say-random-bits-match-the-result/"),
    "xue2026": ("Tian Xue and Jacob P. Covey", "Distributed Shor's algorithm on a modular neutral-atom processor of half a million qubits", "arXiv:2605.03951, May 2026", "https://arxiv.org/abs/2605.03951"),
    "eo14412": ("The White House", "Executive Order 14412 — Securing the nation against advanced cryptographic attacks", "22 June 2026", "https://www.whitehouse.gov/presidential-actions/2026/06/securing-the-nation-against-advanced-cryptographic-attacks/"),
    "lu2026": ("Eric Lu (Cognition)", "Factoring RSA-260 — a GPU port of CADO-NFS, 4,923 GPU-days", "3 September 2026, written up 9 September", "https://cognition.com/blog/factoring-rsa-260"),
    "haner2026": ("Thomas Häner and 13 others (IonQ)", "Computing 256-bit elliptic curve discrete logarithms in 26 days on a fault-tolerant trapped-ion quantum computer with 20,000 qubits", "arXiv:2609.05625, September 2026", "https://arxiv.org/abs/2609.05625"),
    "weis2026": ("Stephen A. Weis (Anthropic)", "Factoring RSA-896 — CADO-NFS on idle data-centre GPUs, about 30 GPU-years in ten days", "19 September 2026", "https://saweis.net/posts/rsa-896.html"),
    "records": ("Wikipedia contributors", "Integer factorization records", "Wikipedia, read September 2026", "https://en.wikipedia.org/wiki/Integer_factorization_records"),
    "schneier2021": ("Bruce Schneier", "No, RSA is not broken — on Schnorr's claim", "Schneier on Security, 5 March 2021", "https://www.schneier.com/blog/archives/2021/03/no-rsa-is-not-broken.html"),
    # ---------------------------------------------------------------- the wallet, 2025–2026
    "chaincode2025": ("Anthony Milton and Clara Shikhelman (Chaincode Labs)", "Bitcoin and quantum computing: current status and future directions", "May 2025", "https://chaincode.com/bitcoin-post-quantum.pdf"),
    "coinshares2026": ("CoinDesk, reporting CoinShares", "The quantum threat to Bitcoin is smaller than people think — 1.6 million BTC in P2PK", "9 February 2026", "https://www.coindesk.com/markets/2026/02/09/the-quantum-threat-to-bitcoin-is-smaller-than-people-think-coinshares"),
    "glassnode2026": ("Glassnode Research, via Yahoo Finance", "6.04 million BTC with the public key already visible on-chain", "May 2026", "https://finance.yahoo.com/markets/crypto/articles/nearly-500b-bitcoin-exposed-future-230004094.html"),
    "coinbase2026": ("The Block, reporting Coinbase's advisory board", "Coinbase quantum report flags exchange cold wallets among millions of bitcoin exposed by address reuse", "13 June 2026", "https://www.theblock.co/news/business/2026-06-13-coinbase-quantum-report-flags-exchange-cold-wallets-among-millions-of-bitcoin-exposed-by-address-reuse-404685"),
    "coinbase2026b": ("CoinDesk", "Coinbase advisory board says the quantum computing threat is on the horizon", "21 April 2026", "https://www.coindesk.com/tech/2026/04/21/coinbase-advisory-board-says-quantum-computing-threat-is-on-the-horizon-crypto-needs-a-plan"),
    "bip361": ("Jameson Lopp, Christian Papathanasiou, Ludovic Perret, Kevin Le Bao and Trevor Ross", "BIP 361 — Post quantum migration and legacy signature sunset", "bitcoin/bips, draft, 2026", "https://github.com/bitcoin/bips/blob/master/bip-0361.mediawiki"),
    "lopp2025list": ("Jameson Lopp", "A post quantum migration proposal", "bitcoindev mailing list, 13 July 2025", "https://groups.google.com/g/bitcoindev/c/uEaf4bj07rE"),
    "hourglass2025": ("Hunter Beast", "Hourglass — rate-limiting spends from pay-to-pubkey outputs", "bitcoindev mailing list, 30 April 2025", "https://groups.google.com/g/bitcoindev/c/zmg3U117aNc/m/lDCMs9j7EAAJ"),
    "dryja2025": ("Tadge Dryja", "A commit-reveal soft fork for spending exposed keys after ECDSA is broken", "bitcoindev mailing list, 29 May 2025", "https://groups.google.com/g/bitcoindev/c/LpWOcXMcvk8"),
    "canary2026": ("CoinDesk, reporting BitMEX Research", "Bitcoin devs float a quantum tripwire that triggers a coin freeze only if an attack is proven", "16 April 2026", "https://www.coindesk.com/tech/2026/04/16/bitcoin-devs-float-quantum-tripwire-that-triggers-coin-freeze-only-if-attack-is-proven"),
    "shrincs2026": ("CoinDesk, reporting Jonas Nick and Mikhail Kudinov (Blockstream)", "SHRINCS — a hash-based post-quantum signature sized for Bitcoin blocks", "27 August 2026", "https://www.coindesk.com/tech/2026/08/27/bitcoin-researchers-propose-quantum-fix-that-would-not-crowd-out-transactions"),
    "optech403": ("Bitcoin Optech", "Newsletter #403 — the post-quantum discussion that week", "1 May 2026", "https://bitcoinops.org/en/newsletters/2026/05/01/"),
    "optech412": ("Bitcoin Optech", "Newsletter #412 — hybrid signatures in BIP-360 leaves", "3 July 2026", "https://bitcoinops.org/en/newsletters/2026/07/03/"),
    "ethroadmap": ("ethereum.org", "Roadmap — quantum resistance", "read September 2026", "https://ethereum.org/roadmap/security/quantum-resistance/"),
    "algorand2025": ("Algorand Foundation", "Quantum-resistant transactions on Algorand with Falcon signatures", "3 November 2025", "https://algorand.co/blog/technical-brief-quantum-resistant-transactions-on-algorand-with-falcon-signatures"),
    "gri2025": ("Michele Mosca and Marco Piani", "Quantum threat timeline report 2025 — the expert survey", "Global Risk Institute and evolutionQ, March 2026; summarised at postquantum.com", "https://postquantum.com/security-pqc/quantum-threat-timeline-report-2025/"),
    "blackrock2025": ("The Quantum Insider", "BlackRock updates its Bitcoin ETF prospectus with a broadened quantum computing warning", "13 May 2025", "https://thequantuminsider.com/2025/05/13/blockrock-updates-bitcoin-etf-with-broadened-warning-about-quantum-computing/"),
    "coindesk2026roadmap": ("CoinDesk", "Google says post-quantum migration needs to happen by 2029 — and Bitcoin has no roadmap", "28 March 2026", "https://www.coindesk.com/tech/2026/03/28/watch-out-bitcoin-devs-google-says-post-quantum-migration-needs-to-happen-by-2029"),
    "p2q": ("Casey Rodarmor", "P2Q — a draft BIP for a SegWit version 3 output whose key path can later be switched off", "draft on GitHub", "https://github.com/casey/bips/blob/bip-p2q/bip-p2q.md"),
    "starkware2026": ("CoinDesk", "Quantum-safe Bitcoin now possible without a soft fork, but costs $200 a pop", "10 April 2026", "https://www.coindesk.com/markets/2026/04/10/quantum-safe-bitcoin-now-possible-without-a-soft-fork-but-costs-usd200-a-pop"),
    "pacts2026": ("CoinDesk", "Provable address-control timestamps — a way to prove control without moving coins", "2 May 2026", "https://www.coindesk.com/tech/2026/05/02/new-bitcoin-quantum-proposal-offers-satoshi-nakamoto-a-way-to-prove-control-without-moving-btc"),
}

BY_ID = {k: i + 1 for i, k in enumerate(SOURCES)}


def url(sid: str) -> str:
    return SOURCES[sid][3]


def cite_html(ids, esc) -> str:
    parts = []
    for sid in ids:
        if sid not in SOURCES:
            raise KeyError(f"unknown source id: {sid}")
        n = BY_ID[sid]
        parts.append(f'<a class="cite" href="#src-{n}" data-src="{esc(sid)}" title="{esc(SOURCES[sid][1])}">[{n}]</a>')
    return "".join(parts)
