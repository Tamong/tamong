#ifndef SOME_HEADER_GUARD_WITH_UNIQUE_NAME
#define SOME_HEADER_GUARD_WITH_UNIQUE_NAME

// Ext3 superblock
typedef struct Superblock_t  {
   uint32_t s_inodes_count;         //!< Total number of inodes
   uint32_t s_blocks_count;         //!< Filesystem size in blocks
   uint32_t s_r_blocks_count;       /* Number of reserved blocks */
   uint32_t s_free_blocks_count;    /* Free blocks count */
   uint32_t s_free_inodes_count;    /* Free inodes count */
   uint32_t s_first_data_block;     /* First Data Block */
   uint32_t s_log_block_size;       /* Block size */
   int32_t  s_log_frag_size;        /* Fragment size */ // was s32(?)
   uint32_t s_blocks_per_group;     //!< Number of blocks per group
   uint32_t s_frags_per_group;      /* # Fragments per group */
   uint32_t s_inodes_per_group;     //!< Number of inodes per group */
   uint32_t s_mtime;                /* Mount time */
   uint32_t s_wtime;                /* Write time */
   uint16_t s_mnt_count;            /* Mount count */
   int16_t  s_max_mnt_count;        /* Maximal mount count */
 
   /*!\brief Magic signature
    *
        * This is the signature of the partition. The ext2 and ext3 partitions
        * have 0xEF53 at this place.
        */
   uint16_t s_magic;                /* Magic signature */
   uint16_t s_state;                /* File system state */
   uint16_t s_errors;               /* Behaviour when detecting errors */
   uint16_t s_minor_rev_level;      /* Minor revision level */
   uint32_t s_lastcheck;            /* time of last check */
   uint32_t s_checkinterval;        /* max. time between checks */
   uint32_t s_creator_os;           /* OS */
   uint32_t s_rev_level;            /* Revision level */
   uint16_t s_def_resuid;           /* Default uid for reserved blocks */
   uint16_t s_def_resgid;           /* Default gid for reserved blocks */

   /* These fields are for EXT2_DYNAMIC_REV superblocks only. */
   uint32_t s_first_ino;            /* First non-reserved inode */
   uint16_t s_inode_size;           /* size of inode structure */
   uint16_t s_block_group_nr;       /* block group # of this superblock */
   uint32_t s_feature_compat;       /* compatible feature set */
   uint32_t s_feature_incompat;     /* incompatible feature set */
   uint32_t s_feature_ro_compat;    /* readonly-compatible feature set */
/*68*/  uint8_t   s_uuid[16];             /* 128-bit uuid for volume */
/*78*/  char  s_volume_name[16];      /* volume name */
/*88*/  char  s_last_mounted[64];     /* directory where last mounted */
/*C8*/  uint32_t  s_algorithm_usage_bitmap; /* For compression */
        /*
         * Performance hints.  Directory preallocation should only
         * happen if the EXT3_FEATURE_COMPAT_DIR_PREALLOC flag is on.
         */
        uint8_t   s_prealloc_blocks;      /* Nr of blocks to try to preallocate*/
        uint8_t   s_prealloc_dir_blocks;  /* Nr to preallocate for dirs */
        uint16_t  s_reserved_gdt_blocks;  /* Per group desc for online growth */
       /*
        * Journaling support valid if EXT3_FEATURE_COMPAT_HAS_JOURNAL set.
        */
/*D0*/  uint8_t   s_journal_uuid[16];     /* uuid of journal superblock */
/*E0*/  uint32_t  s_journal_inum;         /* inode number of journal file */
        uint32_t  s_journal_dev;          /* device number of journal file */
        uint32_t  s_last_orphan;          /* start of list of inodes to delete */
        uint32_t  s_hash_seed[4];         /* HTREE hash seed */
        uint8_t   s_def_hash_version;     /* Default hash version to use */
        uint8_t   s_reserved_char_pad;
        uint16_t  s_reserved_word_pad;
        uint32_t  s_default_mount_opts;
        uint32_t  s_first_meta_bg;        /* First metablock block group */
        uint32_t  s_mkfs_time;            /* When the filesystem was created */
        uint32_t  s_jnl_blocks[17];       /* Backup of the journal inode */
  /* 64bit support valid if EXT4_FEATURE_COMPAT_64BIT */
/*150*/ uint32_t  s_blocks_count_hi;      /* Blocks count */
        uint32_t  s_r_blocks_count_hi;    /* Reserved blocks count */
        uint32_t  s_free_blocks_count_hi; /* Free blocks count */
        uint16_t  s_min_extra_isize;      /* All inodes have at least # bytes */
        uint16_t  s_want_extra_isize;     /* New inodes should reserve # bytes */
        uint32_t  s_flags;                /* Miscellaneous flags */
        uint16_t  s_raid_stride;          /* RAID stride */
        uint16_t  s_mmp_interval;         /* # seconds to wait in MMP checking */
        uint64_t  s_mmp_block;            /* Block for multi-mount protection */
        uint32_t  s_raid_stripe_width;    /* blocks on all data disks (N*stride)*/
        uint8_t   s_log_groups_per_flex;  /* FLEX_BG group size */
        uint8_t   s_reserved_char_pad2;
        uint16_t  s_reserved_pad;
        uint32_t s_pad[162];             /* Padding to the end of the block */
} ext3_super_block  ;

// Ext3 group descriptor
struct ext3_group_desc {
    uint32_t bg_block_bitmap;
    uint32_t bg_inode_bitmap;
    uint32_t bg_inode_table;
    uint16_t bg_free_blocks_count;
    uint16_t bg_free_inodes_count;
    uint16_t bg_used_dirs_count;
    uint16_t bg_pad;
    uint32_t bg_reserved[3];
};

// Ext3 inode
struct ext3_inode {
    uint16_t i_mode;
    uint16_t i_uid;
    uint32_t i_size;
    uint32_t i_atime;
    uint32_t i_ctime;
    uint32_t i_mtime;
    uint32_t i_dtime;
    uint16_t i_gid;
    uint16_t i_links_count;
    uint32_t i_blocks;
    uint32_t i_flags;
    uint32_t i_osd1;
    uint32_t i_block[15];
    uint32_t i_generation;
    uint32_t i_file_acl;
    uint32_t i_dir_acl;
    uint32_t i_faddr;
    uint32_t i_osd2[3];
};

// Ext3 directory entry
struct ext3_dir_entry {
    uint32_t inode;
    uint16_t rec_len;
    uint8_t name_len;
    uint8_t file_type;
    char name[255]; // Can be smaller based on the name_len value
};


#endif