@load base/frameworks/files
@load base/files/hash
@load base/files/extract

module CustomFileExtraction;

export {
    # MIME types to extract and hash
    option mime_type_analysis : set[string] = {
        "application/x-dosexec",        # Windows executables
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/x-rar",
        "application/x-gzip"
    };
}

event file_sniff(f: fa_file, meta: fa_metadata)
    {
    if ( meta?$mime_type && meta$mime_type in mime_type_analysis )
        {
        # Enable full reassembly for this file
        Files::enable_reassembly(f);
        
        # Extend reassembly buffer (10 MB)
        Files::set_reassembly_buffer_size(f, 10 * 1024 * 1024);
        
        # Increase idle timeout for slow transfers
        Files::set_timeout_interval(f, 5mins);
        
        # Set extraction args: no size limit & ignore missing bytes
        local args: Files::AnalyzerArgs = [$extract_limit = 0,
                                           $extract_limit_includes_missing = F,
                                           $extract_filename = fmt("extracted-%s", f$id)];
        
        # Add analyzers for extraction + all hash types
        Files::add_analyzer(f, Files::ANALYZER_EXTRACT, args);
        Files::add_analyzer(f, Files::ANALYZER_MD5);
        Files::add_analyzer(f, Files::ANALYZER_SHA1);
        Files::add_analyzer(f, Files::ANALYZER_SHA256);
        }
    }

event file_hash(f: fa_file, kind: string, hash: string)
    {
    print fmt("HASH | %s | %s | %s", f$id, kind, hash);
    }
