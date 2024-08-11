// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PKI {
    struct Certificate {
        address owner;
        bytes32 certificateHash;
        bool isValid;
    }

    mapping(bytes32 => Certificate) public certificates;

    event CertificateRegistered(address indexed owner, bytes32 indexed certificateHash);
    event CertificateRevoked(address indexed owner, bytes32 indexed certificateHash);

    function registerCertificate(bytes32 _certificateHash) public {
        require(certificates[_certificateHash].owner == address(0), "Certificate already registered.");

        certificates[_certificateHash] = Certificate({
            owner: msg.sender,
            certificateHash: _certificateHash,
            isValid: true
        });

        emit CertificateRegistered(msg.sender, _certificateHash);
    }

    function revokeCertificate(bytes32 _certificateHash) public {
        require(certificates[_certificateHash].owner == msg.sender, "Only the owner can revoke this certificate.");
        require(certificates[_certificateHash].isValid, "Certificate is already revoked.");

        certificates[_certificateHash].isValid = false;

        emit CertificateRevoked(msg.sender, _certificateHash);
    }

    function verifyCertificate(bytes32 _certificateHash) public view returns (bool) {
        return certificates[_certificateHash].isValid;
    }
}
