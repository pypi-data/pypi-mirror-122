#ifndef AWS_IO_PKI_UTILS_H
#define AWS_IO_PKI_UTILS_H
/**
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0.
 */
#include <aws/io/io.h>

#ifdef _WIN32
/* It's ok to include external headers because this is a PRIVATE header file
 * (it is usually a crime to include windows.h from header file) */
#    include <Windows.h>
#endif /* _WIN32 */

#ifdef AWS_OS_APPLE
/* It's ok to include external headers because this is a PRIVATE header file */
#    include <CoreFoundation/CFArray.h>
#endif /* AWS_OS_APPLE */

struct aws_string;

AWS_EXTERN_C_BEGIN

/**
 * Cleans up and securely zeroes out the outputs of 'aws_decode_pem_to_buffer_list()'
 * and 'aws_read_and_decode_pem_file_to_buffer_list()'
 */
AWS_IO_API void aws_cert_chain_clean_up(struct aws_array_list *cert_chain);

/**
 * Decodes a PEM file and adds the results to 'cert_chain_or_key' if successful.
 * Otherwise, 'cert_chain_or_key' will be empty. The type stored in 'cert_chain_or_key'
 * is 'struct aws_byte_buf' by value. This code is slow, and it allocates, so please try
 * not to call this in the middle of something that needs to be fast or resource sensitive.
 */
AWS_IO_API int aws_decode_pem_to_buffer_list(
    struct aws_allocator *alloc,
    const struct aws_byte_cursor *pem_cursor,
    struct aws_array_list *cert_chain_or_key);

/**
 * Decodes a PEM file at 'filename' and adds the results to 'cert_chain_or_key' if successful.
 * Otherwise, 'cert_chain_or_key' will be empty. The type stored in 'cert_chain_or_key'
 * is 'struct aws_byte_buf' by value. This code is slow, and it allocates, so please try
 * not to call this in the middle of something that needs to be fast or resource sensitive.
 */
AWS_IO_API int aws_read_and_decode_pem_file_to_buffer_list(
    struct aws_allocator *alloc,
    const char *filename,
    struct aws_array_list *cert_chain_or_key);

#ifdef AWS_OS_APPLE
#    if !defined(AWS_OS_IOS)
/**
 * Imports a PEM armored PKCS#7 public/private key pair
 * into identity for use with SecurityFramework.
 */
int aws_import_public_and_private_keys_to_identity(
    struct aws_allocator *alloc,
    CFAllocatorRef cf_alloc,
    const struct aws_byte_cursor *public_cert_chain,
    const struct aws_byte_cursor *private_key,
    CFArrayRef *identity,
    const struct aws_string *keychain_path);
#    endif /* AWS_OS_IOS */

/**
 * Imports a PKCS#12 file into identity for use with
 * SecurityFramework
 */
int aws_import_pkcs12_to_identity(
    CFAllocatorRef cf_alloc,
    const struct aws_byte_cursor *pkcs12_cursor,
    const struct aws_byte_cursor *password,
    CFArrayRef *identity);

/**
 * Loads PRM armored PKCS#7 certificates into certs
 * for use with custom CA.
 */
int aws_import_trusted_certificates(
    struct aws_allocator *alloc,
    CFAllocatorRef cf_alloc,
    const struct aws_byte_cursor *certificates_blob,
    CFArrayRef *certs);

/**
 * Releases identity (the output of the aws_import_* functions).
 */
void aws_release_identity(CFArrayRef identity);

/**
 * releases the output of aws_import_trusted_certificates.
 */
void aws_release_certificates(CFArrayRef certs);

#endif /* AWS_OS_APPLE */

#ifdef _WIN32

/**
 * Returns AWS_OP_SUCCESS if we were able to successfully load the certificate and cert_store.
 *
 * Returns AWS_OP_ERR otherwise.
 */
AWS_IO_API int aws_load_cert_from_system_cert_store(
    const char *cert_path,
    HCERTSTORE *cert_store,
    PCCERT_CONTEXT *certs);

/**
 * Imports a PEM armored PKCS#7 blob into an ephemeral certificate store for use
 * as a custom CA.
 */
AWS_IO_API int aws_import_trusted_certificates(
    struct aws_allocator *alloc,
    const struct aws_byte_cursor *certificates_blob,
    HCERTSTORE *cert_store);

/**
 * Closes a cert store that was opened by aws_is_system_cert_store, aws_import_trusted_certificates,
 * or aws_import_key_pair_to_cert_context.
 */
AWS_IO_API void aws_close_cert_store(HCERTSTORE cert_store);

/**
 * Imports a PEM armored PKCS#7 public/private key pair into certs for use as a certificate with SSPI.
 */
AWS_IO_API int aws_import_key_pair_to_cert_context(
    struct aws_allocator *alloc,
    const struct aws_byte_cursor *public_cert_chain,
    const struct aws_byte_cursor *private_key,
    bool is_client_mode,
    HCERTSTORE *cert_store,
    PCCERT_CONTEXT *certs,
    HCRYPTPROV *crypto_provider,
    HCRYPTKEY *private_key_handle);

#endif /* _WIN32 */

AWS_EXTERN_C_END

#endif /* AWS_IO_PKI_UTILS_H */
