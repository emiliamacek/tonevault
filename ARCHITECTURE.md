# Software Architecture & Design Patterns

This document outlines the enterprise design patterns implemented in the **ToneVault** project to ensure clean code, maintainability, and scalability.

## 1. Domain Logic Patterns

### 1.1 Service Layer
* **Implementation:** `SetupService`, `EquipmentService` (located in `services.py`).
* **Rationale:** Business logic (e.g., adding gear to a signal chain, calculating statistics, validating ownership upon deletion) is decoupled from the Views.
* **Benefits:** Unloads the `views.py` file, making the code more readable, highly testable, and allowing the same logic to be reused across different parts of the application (e.g., API endpoints vs. Web Views).

### 1.2 Domain Model
* **Implementation:** `Setup`, `OwnedGear`, `Guitar`, `Amplifier`, `Pedal`, `SignalChainItem`.
* **Rationale:** These classes represent real-world musical concepts. They are not just data containers; they possess relationships and specific behaviors (e.g., the `gear_item` property in `OwnedGear` dynamically resolving the gear type).
* **Benefits:** Maps real-world objects into code using object-oriented principles rather than raw database records.

## 2. Data Source Architectural Patterns

### 2.1 Active Record
* **Implementation:** All models in `models.py` inheriting from `django.db.models.Model`.
* **Rationale:** Each model object wraps a row in a database table, encapsulating database access and adding domain logic on that data.
* **Benefits:** Simplicity and speed in performing CRUD operations without writing raw SQL queries.

## 3. Object-Relational Metadata Mapping Patterns

### 3.1 Repository
* **Implementation:** `OwnedGearRepository`, `BrandRepository`, `GuitarRepository` (located in `repositories.py`).
* **Rationale:** Acts as an intermediary layer between the domain and data mapping. Methods like `filter_gear` or `get_user_brands` hide complex ORM queries.
* **Benefits:** Centralizes query logic. If the filtering mechanism changes, it only needs to be updated in the Repository, keeping the Views clean.

### 3.2 Query Object
* **Implementation:** Django's `Q` objects used within the repositories (e.g., `Q(guitar__brand_id=brand_id)`).
* **Rationale:** Complex filtering queries (searching by name, type, brand) are built as objects that can be dynamically chained and combined using logical operators.
* **Benefits:** Allows building advanced database filters in a flexible, object-oriented way.

### 3.3 Metadata Mapping
* **Implementation:** Model field definitions in `models.py` (e.g., `name = models.CharField(...)`).
* **Rationale:** Metadata about how classes map to database tables (column types, constraints) are defined directly within the class code via the Django ORM.
* **Benefits:** Automatic database schema generation (migrations) and data validation at the application level.

## 4. Structural Patterns for Object-Relational Mapping

### 4.1 Identity Field
* **Implementation:** The implicit `id` (Primary Key) field in all models.
* **Rationale:** Every object has a unique identifier that links the in-memory object to a specific database row.
* **Benefits:** Enables unambiguous object identification and relationship management.

### 4.2 Foreign Key Mapping
* **Implementation:** `Setup.user`, `OwnedGear.guitar`, `Song.band`.
* **Rationale:** Relationships between objects (e.g., a Setup belongs to a User) are mapped to foreign keys in the relational database.
* **Benefits:** Ensures data integrity and provides easy navigation through relationships in the code.

### 4.3 Association Table Mapping
* **Implementation:** The `SignalChainItem` model.
* **Rationale:** The Many-to-Many relationship between `Setup` and `OwnedGear` required additional context (e.g., the `order` in the chain, specific `settings` knobs). This is mapped as a separate joining class/table.
* **Benefits:** Allows storing attributes of the relationship itself, rather than just the fact that two objects are connected.

## 5. Web Presentation Patterns

### 5.1 Model View Controller (MVC)
* **Implementation:** The overall project structure (Django's MVT: Model=`models.py`, View=`templates/`, Controller=`views.py`).
* **Rationale:** Divides responsibilities into data handling (Model), presentation (Templates), and request routing/control logic (Views).
* **Benefits:** Separation of concerns, easier code management, and independent frontend/backend development.

### 5.2 Template View
* **Implementation:** HTML files (e.g., `list.html`, `profile.html`).
* **Rationale:** Views render dynamic HTML pages by injecting model data into templates using template tags.
* **Benefits:** Dynamic UI generation based on database states.

### 5.3 Page Controller
* **Implementation:** Class-Based Views like `SetupListView`, `OwnedGearDetailView` in `views.py`.
* **Rationale:** Each web page has a dedicated view class or function that handles the specific HTTP request, fetches necessary data, and selects the template.
* **Benefits:** Clear division of handling logic for individual application pages.

## 6. Base and Concurrency Patterns

### 6.1 Layer Supertype
* **Implementation:** `BaseRepository` in `common/repositories.py` and Django's generic views.
* **Rationale:** A base class for repositories to define common methods (e.g., `_get_base_queryset`) inherited by all subclasses in that layer.
* **Benefits:** Prevents code duplication and ensures a consistent interface across the architectural layer.

### 6.2 Lazy Load
* **Implementation:** Django ORM's QuerySet evaluation (e.g., accessing `setup.signalchainitem_set.all()` in a template).
* **Rationale:** Data from related tables is not fetched from the database when the primary object is queried, but only later when specifically requested.
* **Benefits:** Increased application performance by avoiding unnecessary data retrieval.

### 6.3 Server Session State
* **Implementation:** Django's authentication and session backend (`request.user`).
* **Rationale:** The user's login state is stored on the server side (in the session database), while the client only holds a session identifier (cookie).
* **Benefits:** Secure session data storage and the ability to maintain state across stateless HTTP requests.
