drop table post
drop table postcomment

create table dbo.post(
[Id] bigint NOT NULL,
[title] [nvarchar](max) NULL,
[author] [nvarchar](100) NULL,
[date] datetime NULL,
[content] ntext NULL,
[ip] [nvarchar](50) NULL,
[score] int NULL,
[Url] [nvarchar](max) NULL
CONSTRAINT [PK_post] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)
)


create table dbo.postcomment(
[Id] [uniqueidentifier] NOT NULL,
[postId] bigint NOT NULL,
[user] [nvarchar](100) NULL,
[content] ntext NULL,
[score] int NULL,
[ip] nvarchar(200) null,
[commenttime] nvarchar(100) null,
CONSTRAINT [PK_postcomment] PRIMARY KEY CLUSTERED 
(
	[Id] ASC,
	[postId] ASC
)
)

ALTER TABLE [dbo].[postcomment]  WITH CHECK ADD  CONSTRAINT [FK_postcomment_postId] FOREIGN KEY([postId])
REFERENCES [dbo].[post] ([Id])
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[postcomment] CHECK CONSTRAINT [FK_postcomment_postId]
GO

ALTER TABLE [dbo].[postcomment] add crtdate datetime not null default (getdate());
ALTER TABLE [dbo].[post] add crtdate datetime not null default (getdate());

--政黑
create table dbo.post_police(
[Id] bigint NOT NULL,
[title] [nvarchar](max) NULL,
[author] [nvarchar](100) NULL,
[date] datetime NULL,
[content] ntext NULL,
[ip] [nvarchar](50) NULL,
[score] int NULL,
[Url] [nvarchar](max) NULL
CONSTRAINT [PK_post_police] PRIMARY KEY CLUSTERED 
(
	[Id] ASC
)
)


create table dbo.postcomment_police(
[Id] [uniqueidentifier] NOT NULL,
[postId] bigint NOT NULL,
[user] [nvarchar](100) NULL,
[content] ntext NULL,
[score] int NULL,
[ip] nvarchar(200) null,
[commenttime] nvarchar(100) null,
CONSTRAINT [PK_postcomment_police] PRIMARY KEY CLUSTERED 
(
	[Id] ASC,
	[postId] ASC
)
)

ALTER TABLE [dbo].[postcomment_police]  WITH CHECK ADD  CONSTRAINT [FK_postcomment_police_postId] FOREIGN KEY([postId])
REFERENCES [dbo].[post_police] ([Id])
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[postcomment_police] CHECK CONSTRAINT [FK_postcomment_police_postId]
GO

ALTER TABLE [dbo].[postcomment_police] add crtdate datetime not null default (getdate());
ALTER TABLE [dbo].[post_police] add crtdate datetime not null default (getdate());
