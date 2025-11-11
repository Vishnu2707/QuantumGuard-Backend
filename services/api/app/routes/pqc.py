
from fastapi import APIRouter, Depends, HTTPException, Request
from ..models import (
    PQCKEMKeypairIn, PQCKEMEncapIn, PQCKEMDecapIn,
    PQCSigKeypairIn, PQCSigSignIn, PQCSigVerifyIn
)
from ..deps import api_key_owner_id
from ..utils import log_api_call
import oqs, binascii, time

router = APIRouter(prefix="/v1/pqc", tags=["pqc"])

# --- KEM ---
@router.post("/kem/keypair")
async def kem_keypair(body: PQCKEMKeypairIn, request: Request, user_id: str = Depends(api_key_owner_id)):
    started = time.time()
    alg = body.scheme
    try:
        with oqs.KeyEncapsulation(alg) as kem:
            pk = kem.generate_keypair()
            sk = kem.export_secret_key()
        resp = {
            "publicKey": binascii.hexlify(pk).decode(),
            "secretKey": binascii.hexlify(sk).decode()
        }
        await log_api_call(user_id, "/v1/pqc/kem/keypair", alg, 200, started)
        return resp
    except Exception as e:
        await log_api_call(user_id, "/v1/pqc/kem/keypair", alg, 500, started)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/kem/encap")
async def kem_encap(body: PQCKEMEncapIn, request: Request, user_id: str = Depends(api_key_owner_id)):
    started = time.time()
    alg = body.scheme
    try:
        with oqs.KeyEncapsulation(alg) as kem:
            pk = binascii.unhexlify(body.publicKey)
            ct, ss = kem.encap_secret(pk)
        resp = {
            "ciphertext": binascii.hexlify(ct).decode(),
            "sharedSecret": binascii.hexlify(ss).decode()
        }
        await log_api_call(user_id, "/v1/pqc/kem/encap", alg, 200, started)
        return resp
    except Exception as e:
        await log_api_call(user_id, "/v1/pqc/kem/encap", alg, 500, started)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/kem/decap")
async def kem_decap(body: PQCKEMDecapIn, request: Request, user_id: str = Depends(api_key_owner_id)):
    started = time.time()
    alg = body.scheme
    try:
        with oqs.KeyEncapsulation(alg) as kem:
            kem.import_secret_key(binascii.unhexlify(body.secretKey))
            ct = binascii.unhexlify(body.ciphertext)
            ss = kem.decap_secret(ct)
        resp = {"sharedSecret": binascii.hexlify(ss).decode()}
        await log_api_call(user_id, "/v1/pqc/kem/decap", alg, 200, started)
        return resp
    except Exception as e:
        await log_api_call(user_id, "/v1/pqc/kem/decap", alg, 500, started)
        raise HTTPException(status_code=500, detail=str(e))

# --- Signatures ---
@router.post("/sig/keypair")
async def sig_keypair(body: PQCSigKeypairIn, request: Request, user_id: str = Depends(api_key_owner_id)):
    started = time.time()
    alg = body.scheme
    try:
        with oqs.Signature(alg) as sig:
            pk = sig.generate_keypair()
            sk = sig.export_secret_key()
        resp = {
            "publicKey": binascii.hexlify(pk).decode(),
            "secretKey": binascii.hexlify(sk).decode()
        }
        await log_api_call(user_id, "/v1/pqc/sig/keypair", alg, 200, started)
        return resp
    except Exception as e:
        await log_api_call(user_id, "/v1/pqc/sig/keypair", alg, 500, started)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sig/sign")
async def sig_sign(body: PQCSigSignIn, request: Request, user_id: str = Depends(api_key_owner_id)):
    started = time.time()
    alg = body.scheme
    try:
        with oqs.Signature(alg) as sig:
            sig.import_secret_key(bytes.fromhex(body.secretKey))
            signature = sig.sign(body.message.encode())
        resp = {"signature": signature.hex()}
        await log_api_call(user_id, "/v1/pqc/sig/sign", alg, 200, started)
        return resp
    except Exception as e:
        await log_api_call(user_id, "/v1/pqc/sig/sign", alg, 500, started)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sig/verify")
async def sig_verify(body: PQCSigVerifyIn, request: Request, user_id: str = Depends(api_key_owner_id)):
    started = time.time()
    alg = body.scheme
    try:
        with oqs.Signature(alg) as sig:
            ok = sig.verify(body.message.encode(), bytes.fromhex(body.signature), bytes.fromhex(body.publicKey))
        resp = {"valid": bool(ok)}
        await log_api_call(user_id, "/v1/pqc/sig/verify", alg, 200, started)
        return resp
    except Exception as e:
        await log_api_call(user_id, "/v1/pqc/sig/verify", alg, 500, started)
        raise HTTPException(status_code=500, detail=str(e))
