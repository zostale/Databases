DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS Bids;
DROP TABLE IF EXISTS CategoryList;

CREATE TABLE Item(
	ItemID INTEGER PRIMARY KEY,
	SellerID TEXT NOT NULL,
	Name TEXT NOT NULL,
	Buy_Price REAL,
	First_Bid REAL NOT NULL,
	Started DATETIME,
	Ends DATETIME CHECK (Ends > Starts),
	Description TEXT NOT NULL,
	FOREIGN KEY(SellerID) REFERENCES User(UserID)

);
CREATE TABLE User(
	UserID TEXT PRIMARY KEY,
	Location TEXT,
	Country TEXT,
	Rating INTEGER
);
CREATE TABLE Category(
	ItemID INTEGER NOT NULL,
	Category TEXT NOT NULL,
	CONSTRAINT unique_item_category UNIQUE (ItemID, Category),
	FOREIGN KEY (Category) REFERENCES CategoryList(Category),
	FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);
CREATE TABLE Bids(
	UserID TEXT NOT NULL,
	Time DATETIME NOT NULL,
	Amount REAL NOT NULL
	ItemID INTEGER NOT NULL,
	FOREIGN KEY (UserID) REFERENCES User(UserID),
	FOREIGN KEY (ItemID) REFERENCES Item(ItemID)
);
CREATE TABLE CategoryList(
	Category TEXT PRIMARY KEY
);
