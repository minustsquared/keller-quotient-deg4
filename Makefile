.PHONY: verify certify sha256 clean-out

verify:
	python3 04-scripts/generate_and_certify.py
	python3 04-scripts/emit_exhaustiveness_check.py
	python3 04-scripts/verify_certificates.py

certify: out
	Singular 05-solver-inputs/certify_exhaustiveness.sing | tee out/certify.log
	M2 --script 05-solver-inputs/deg4_decomposition.m2 | tee out/m2.log

out:
	mkdir -p out

sha256: out
	shasum -a 256 03-certificates/*.json 03-certificates/transcript.log \
	  05-solver-inputs/*.sing 05-solver-inputs/*.m2 \
	  out/certify.log out/m2.log out/version_manifest.txt \
	  > out/SHA256SUMS.txt

clean-out:
	rm -rf out
