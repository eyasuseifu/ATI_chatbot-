def test_save_user_message(mock_firestore):
    from database.firebase_handler import save_user_message
    
    # Test data
    save_user_message("123", "test_user", "Hello", "Hi there!")
    
    # Verify Firestore write
    doc = mock_firestore.collection("messages").document("123").get()
    assert doc.exists
    assert doc.to_dict()["username"] == "test_user"
    