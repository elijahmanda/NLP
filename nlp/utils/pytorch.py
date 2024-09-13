import torch


def one_hot_encode(labels: torch.Tensor, num_classes: int) -> torch.Tensor:
    """Converts a 1D tensor of labels to a 2D one-hot encoded tensor."""
    return torch.nn.functional.one_hot(labels, num_classes=num_classes)


def normalize(X: torch.Tensor, axis: int = 0) -> torch.Tensor:
    """Normalizes a 2D tensor along a specified axis."""
    mean = torch.mean(X, dim=axis, keepdim=True)
    std = torch.std(X, dim=axis, keepdim=True)
    return (X - mean) / std


def sigmoid(X: torch.Tensor) -> torch.Tensor:
    """Applies the sigmoid function element-wise to a tensor."""
    return torch.sigmoid(X)


def relu(X: torch.Tensor) -> torch.Tensor:
    """Applies the ReLU function element-wise to a tensor."""
    return torch.nn.functional.relu(X)


def softmax(X: torch.Tensor) -> torch.Tensor:
    """Applies the softmax function to a tensor."""
    return torch.nn.functional.softmax(X, dim=1)


def binary_crossentropy(y_true: torch.Tensor, y_pred: torch.Tensor) -> torch.Tensor:
    """Computes the binary cross-entropy loss between two tensors."""
    return torch.mean(-y_true * torch.log(y_pred + 1e-9) - (1 - y_true) * torch.log(1 - y_pred + 1e-9))


def categorical_crossentropy(y_true: torch.Tensor, y_pred: torch.Tensor) -> torch.Tensor:
    """Computes the categorical cross-entropy loss between two tensors."""
    return torch.mean(-y_true * torch.log(y_pred + 1e-9))


def accuracy(y_true: torch.Tensor, y_pred: torch.Tensor) -> float:
    """Computes the classification accuracy between two tensors."""
    return torch.mean(torch.argmax(y_true, dim=1) == torch.argmax(y_pred, dim=1)).item()


def init_weights(module: torch.nn.Module):
    """Initializes the weights of a PyTorch module."""
    if isinstance(module, torch.nn.Linear):
        torch.nn.init.xavier_uniform_(module.weight)
        module.bias.data.fill_(0.01)


def freeze_weights(module: torch.nn.Module):
    """Freezes the weights of a PyTorch module."""
    for param in module.parameters():
        param.requires_grad = False


def unfreeze_weights(module: torch.nn.Module):
    """Unfreezes the weights of a PyTorch module."""
    for param in module.parameters():
        param.requires_grad = True


def count_parameters(module: torch.nn.Module) -> int:
    """Counts the number of trainable parameters in a PyTorch module."""
    return sum(p.numel() for p in module.parameters() if p.requires_grad)


def train(
    model: torch.nn.Module,
    train_loader: torch.utils.data.DataLoader,
    criterion: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
):
    """Trains a PyTorch model for one epoch."""
    model.train()
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()


def evaluate(
    model: torch.nn.Module,
    val_loader: torch.utils.data.DataLoader,
    criterion: torch.nn.Module,
) -> float:
    """Evaluates a PyTorch model on a validation set."""
    model.eval()
    total_loss = 0.0
    total_accuracy = 0.0
    with torch.no_grad():
        for inputs, targets in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            accuracy = (torch.argmax(outputs, dim=1) ==
                        targets).float().mean().item()
            total_loss += loss.item()
            total_accuracy += accuracy
    avg_loss = total_loss / len(val_loader)
    avg_accuracy = total_accuracy / len(val_loader)
    return avg_loss, avg_accuracy

# The init_weights function initializes the weights of a PyTorch module using the Xavier initialization method and sets the bias terms to 0.01.

# The freeze_weights function freezes the weights of a PyTorch module by setting the requires_grad attribute of each parameter to False.

# The unfreeze_weights function unfreezes the weights of a PyTorch module by setting the requires_grad attribute of each parameter to True.

# The count_parameters function counts the number of trainable parameters in a PyTorch module.

# The train function trains a PyTorch model for one epoch using a specified training data loader, loss criterion, and optimizer.

# The evaluate function evaluates a PyTorch model on a validation set using a specified validation data loader and loss criterion. It returns the average loss and accuracy over the validation set.
