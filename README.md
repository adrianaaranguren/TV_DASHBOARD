# TV Dashboard

A simple, single-screen dashboard that displays key metrics from your MongoDB database.

## Features

- **Top 5 Callers This Week**: Shows the most active callers based on call data
- **Top 5 Bookers This Week**: Shows the most active bookers based on deal creation
- **Discos Scheduled This Month**: Total count of deals created this month
- **Discos Held This Month**: Total count of deals that entered "Disco Held" stage this month

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure User Names**:
   Edit the `USER_ID_TO_NAME` dictionary in `app.py` to map user IDs to actual names:
   ```python
   USER_ID_TO_NAME = {
       123: "John Doe",
       456: "Jane Smith",
       # Add more mappings as needed
   }
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Dashboard**:
   Open your browser and go to `http://localhost:5000`

## Configuration

### MongoDB Collections
The application expects two collections in your MongoDB database:
- `calls` - for call data
- `deals` - for deal data

If your collections have different names, update the collection names in `app.py`:
```python
calls_collection = db.your_calls_collection_name
deals_collection = db.your_deals_collection_name
```

### Date Fields
The application looks for these date fields in your documents:
- `createdAt` - for call and deal creation dates
- `stageHistory` - for deal stage history (array with `stage` and `date` fields)

If your documents use different field names, update the field names in the MongoDB aggregation pipelines in `app.py`.

## Features

- **Auto-refresh**: The dashboard automatically refreshes every 30 seconds
- **Responsive Design**: Works on different screen sizes
- **Real-time Data**: Uses current date/time for filtering
- **Error Handling**: Displays errors if database connection fails

## Deployment Options

For production deployment without requiring a computer to run:

1. **Cloud Hosting**: Deploy to services like:
   - Heroku
   - DigitalOcean
   - AWS EC2
   - Google Cloud Platform

2. **Docker**: Create a Docker container for easy deployment

3. **Raspberry Pi**: Run on a Raspberry Pi for a dedicated dashboard display

## Troubleshooting

- **Connection Issues**: Check your MongoDB connection string and network access
- **No Data**: Verify collection names and field names match your database structure
- **User Names**: Make sure to populate the `USER_ID_TO_NAME` dictionary with actual user mappings

## Data Structure Requirements

### Calls Collection
Expected fields:
- `ownerId`: User ID of the caller
- `createdAt`: Date when the call was created

### Deals Collection
Expected fields:
- `createdById`: User ID of the person who created the deal
- `createdAt`: Date when the deal was created
- `stageHistory`: Array of stage changes with `stage` and `date` fields 