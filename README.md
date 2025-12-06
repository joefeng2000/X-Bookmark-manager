# X-Bookmark-manager
a standalone bookmark manager for twitter
Version: 1.0

 Date: September 26, 2025

### 1. Introduction

### 1.1 Project Background

 The official bookmarking functionality provided by X.com (formerly Twitter) is relatively basic and lacks effective categorization, tagging and search capabilities. When the number of bookmarks grows, it becomes very difficult to manage and review them. This project aims to develop a standalone desktop or web application to migrate bookmarks data to the local area for fine-grained management by calling X.com's official API, thus completely solving the pain points of the official tool.

### 1.2 Project Objectives

- **Data Ownership**: Migrate X bookmarks data from the cloud to user-controllable local storage, ensuring data security and permanent access.
- **Efficient Management**: Provide powerful categorization, labeling, searching and editing functions to turn bookmarks into a personal knowledge base.
- **Process automation**: Simplify the process of pulling and cleaning bookmarks from the X platform automatically and in batches.
- **Good experience**: Provide an intuitive and clear user interface with real-time feedback on processing progress to enhance the user experience.

### 1.3 Target Users

 This project mainly targets in-depth X users, who frequently use the bookmark function to collect information, and are troubled by the inadequacy of the existing function, and hope to have a more powerful and private bookmark management program.

### 1.4 Definition of Terms

- **X API**: The official application programming interface provided by X.com.
- **Local Manager**: refers to the bookmarks management application developed by this project, which runs in the user's local environment.
- **Migration**: The process of pulling bookmarks from the X.com platform to the Local Manager and removing them from X.com.
- **Bookmark Entity**: refers to an independent bookmark record, which contains information such as tweet ID, content, author, time, etc.

### 2. Overall Description

### 2.1 Product Vision

 This tool is a desktop or web application that treats X.com as a temporary "bookmark inbox". Users can run the tool periodically to "receive" new bookmarks from the "inbox" - i.e., securely transfer them to a powerful local knowledge base and locally archive, organize and retrieve them. archiving, organizing and retrieving locally.

### 2.2 System Core Workflow

 The core of the system is a **batch, cyclic** migration process designed to bypass the API's limit of 800 latest bookmarks at a time and achieve full or incremental synchronization.

1. **Authentication and initialization**: Users authorize the tool with OAuth to gain access to their X-account bookmarks.
2. **Start Migration Task**: Users manually start a migration task.
3. **Batch fetch**: The tool calls the X API to fetch the latest **bookmarks** from the X account.
    - The tool calls the X API to fetch up to 800 bookmarks by pagination (up to 100 per page), starting with the newest bookmark.
    - The API call needs to handle `pagination_token` properly in order to page correctly.
4. **Secure storage**.
    - The program parses the data of the 800 bookmarks fetched and stores them **completely and atomically** in the local database.
    - An internal status such as `is_synced = true is logged` for each successfully deposited bookmark.
    - **Critical**: You must ensure that the data has been successfully deposited before proceeding to the next step.
5. **Delete on a case-by-case basis**.
    - For bookmarks that have been marked locally as `is_synced`, the program begins calling the X API to delete them from the user's list of bookmarks on the X platform.
    - The deletion operation will strictly adhere to the rate limit (e.g. one deletion every 20 seconds, well below the 50 deletions every 15 minutes).
    - The UI interface should display information about the bookmarks being deleted and the overall progress in real time.
6. **Loop or End**.
    - When a batch (800) of bookmarks has been successfully deleted, the program will automatically re-execute step 3 to get the "new" 800 bookmarks (which are actually older bookmarks that are older in time).
    - This cycle will continue until the API returns an empty list of bookmarks, indicating that all of the user's bookmarks on the X platform have been migrated.
7. **Incremental Update**: For non-first-time users, this process will only migrate bookmarks that have been added since the last synchronization.

### 3. Functional Requirements

### 3.1 Data Synchronization and Migration Module

- **3.1.1 User Authentication**.
    - The system should support user authentication and authorization through X.com's OAuth 2.0.
    - User `access token` and `refresh token` should be stored securely.
- **3.1.2 Bookmark Acquisition**.
    - It should be able to correctly handle paging logic and get up to 800 bookmarks at one time.
    - It should be able to parse the JSON data returned by the API and extract the complete tweet information (see 5. Data Model Design).
- **3.1.3 Local Storage**.
    - The system must confirm that the bookmark data has been successfully written to the local database before allowing the deletion operation.
    - There should be a data validation mechanism to ensure that the stored information is complete and error-free.
- **3.1.4 Bookmark deletion**.
    - Deletion rate can be adjusted by the user in the settings (to provide a safe range).
    - Deletion operations must have a detailed log record, the failure of the request should be added to the retry queue.
- **3.1.5 Migration process control**.
    - There should be clear "Start Migration", "Pause" and "Continue" buttons on the UI.
    - Real-time display of migration progress, such as "Batch 2 / Total 5: Fetching data...", "Deleting: Deleting data. and "Deleting: 150/800...". The log window provides a clear view of the data being acquired.
    - Provide a clear log window to show the operation status of each step.

### 3.2 Local Bookmarks Management Module

- **3.2.1 Bookmark Display**.
    - Support list view and card view modes.
    - Each bookmark should clearly display the author's avatar, nickname, ID, tweet content, release time, media (image/video) thumbnail.
- **3.2.2 Sorting and Filtering**.
    - By default, bookmarks are sorted in reverse order by "bookmark time" (i.e. the newest ones are at the top).
    - Support sorting by "tweet time" in forward/reverse order.
    - Support filtering by author, tags and folders.
- **3.2.3 Search Function**.
    - Provide global search box, support full-text search for tweets and author nicknames/IDs.
    - Support advanced search syntax, such as `tag:technology folder:programming`.
- **3.2.4 Folder Management**.
    - Users can create, rename, and delete folders.
    - Supports multi-level folders (tree structure).
    - Users can drag and drop or move one or more bookmarks to a specified folder.
- **3.2.5 Tag Management**.
    - Users can add one or more tags for each bookmark.
    - Supports creating, renaming, and deleting tags.
    - Provide tag cloud or tag list, click to filter out all bookmarks containing the tag.
- **3.2.6 Bookmark Operations**.
    - **Open Original Link**: Click the link on the bookmark card to open the original tweet in the system default browser.
    - **Delete Locally**: Users can delete bookmarks that are no longer needed from the local manager (this operation does not affect the X platform).
    - **Add Note**: Users can add a personal note or note for each bookmark.

### 4. Non-Functional Requirements

- **4.1 Performance Requirements**.
    - The UI interface responds smoothly and does not lag due to background migration tasks.
    - When the number of bookmarks reaches tens of thousands in the local database, the response time of searching and filtering should be less than 2 seconds.
- **4.2 Reliability and robustness**.
    - The migration process must be designed as a transactional operation. If the program exits accidentally during the deletion process, it should be able to identify which bookmarks have been deleted locally but not in X after restart and continue to perform the deletion task.
    - Provide sound error handling for all API calls (e.g., network outages, API rate overruns, expired authorizations, etc.) and provide clear prompts to the user.
- **4.3 Data Security**.
    - User API credentials must be encrypted and stored locally.
    - Provide manual or automatic local database backup and recovery functions.
- **4.4 User Experience**.
    - The interface design is simple, intuitive and easy to use.
    - Before key operations (e.g. starting full migration, deleting folders), there should be a second confirmation prompt.

### 5. Data Model Design (Recommendation)

 Suggested core fields for the `Bookmarks` table in the local database:

- tweet_id (String, Primary Key) // Unique ID of the tweet
- text (String) // Content of the tweet
- author_id (String) // Author ID
- author_name (String) // Author nickname
- author_handle (String) // author_username (@handle)
- author_avatar_url (String) // link to the author's avatar
- created_at (Timestamp) // the time the tweet was originally published
- bookmarked_at (Timestamp) // the time the user bookmarked the tweet (may not be provided by the X API, but can be pulled instead)
- original_at (Timestamp) // the time the user bookmarked the tweet. may not be provided by the X API, but can be pulled instead)
- original_url (String) // The link to the original tweet - media_urls (JSON/Array) // The links to images, videos, etc. that are included
- local_tags (Array) // A list of tags added locally by the user - local_folder_id ( String) // ID of the folder to which it belongs (foreign key)
- local_notes (Text) // Notes added by the user
- sync_status (Enum) // Synchronization status, e.g., 'synced', 'pending_delete'`

### 6. API Dependencies and Limitations

- **Authentication**: OAuth 1.0
- **Bookmarks fetch**: `GET /2/users/:id/bookmarks`
    - Pagination Limit: Maximum 100 entries per page.
    - Total Limit: Up to 800 latest bookmarks can be retrieved per authentication session (from the beginning).
- **Bookmark deletion**: `DELETE /2/users/:id/bookmarks/:tweet_id`
    - Rate limit: 50 requests every 15 minutes.
